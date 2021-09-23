# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import absolute_import, division, print_function, unicode_literals

import json

import cast_unknown as cast
import six
from .. import compat
from ..model import ImageInfo
from ..server.web import upload_image
from .core import SelectionAttachment

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Tuple


class SelectionImage(SelectionAttachment):
    """Image feature for selection."""

    def _set_v5_2(self, path, field="image"):
        # type: (Text, Text) -> ImageInfo
        select = self.select
        image = upload_image(path, select.module.database.name, select.token)

        # Server need strange data format for image field in cgteamwork5.2
        select.set_fields(
            **{
                field: dict(
                    path=path,
                    max=[image.max],
                    min=[image.min],
                )
            }
        )
        return image

    def _set_v6_1(self, path, field="image"):
        # type: (Text, Text) -> ImageInfo
        select = self.select
        image = upload_image(path, select.module.database.name, select.token)

        select.set_fields(
            **{
                field: json.dumps(
                    [
                        dict(
                            type="image",
                            max=image.max,
                            min=image.min,
                            att_id=image.attachment_id,
                        )
                    ]
                )
            }
        )
        return image

    def set(self, path, field="image"):
        # type: (Text, Text) -> ImageInfo
        """Set image for the field.

        Args:
            field (six.text_type): Defaults to 'image', Server defined field name,
            path (six.text_type): File path.

        Returns:
            ImageInfo: Uploaded image.
        """

        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._set_v5_2(path, field)
        return self._set_v6_1(path, field)

    def get(self, field="image"):
        # type: (Text) -> Tuple[ImageInfo, ...]
        """Get imageinfo used on the field.

        Args:
            field (six.text_type): Defaults to 'image', Server defined field name,

        Returns:
            tuple[ImageInfo]: Image information.
        """

        select = self.select
        ret = set()
        rows = cast.list_(select[field], (str, six.text_type))
        for row in rows:
            try:
                for data in cast.list_(json.loads(row), dict):
                    info = ImageInfo(
                        max=cast.list_(data["max"], (six.text_type, str))[0],
                        min=cast.list_(data["min"], (six.text_type, str))[0],
                        path=data.get("path"),
                        attachment_id=data.get("att_id"),
                    )
                    ret.add(info)
            except (TypeError, KeyError, ValueError):
                continue
        ret = tuple(sorted(ret))
        return ret

    def get_one(self, field="image"):
        # type: (str) -> ImageInfo
        """Get single imageinfo used on the field.

        Args:
            field (six.text_type): Defaults to 'image', Server defined field name,

        Raises:
            ValueError: No image data.
            AssertError: Multiple image data.

        Returns:
            ImageInfo: Image information.
        """
        try:
            images = self.get(field)
            assert len(images) == 1, "Multiple image on the selection."
            return images[0]
        except IndexError:
            raise ValueError("No image on this selection.")
