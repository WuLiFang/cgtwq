# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json

from ..model import ImageInfo
from ..server.web import upload_image
from .core import SelectionAttachment


class SelectionImage(SelectionAttachment):
    """Image feature for selection.  """

    def set(self, path, field='image'):
        """Set image for the field.

        Args:
            field (six.text_type): Defaults to 'image', Server defined field name,
            path (six.text_type): File path.

        Returns:
            ImageInfo: Uploaded image.
        """
        select = self.select
        image = upload_image(path, select.module.database.name, select.token)

        # Server need strange data format for image field in cgteamwork5.2
        select.set_fields(
            **{field: dict(path=path, max=[image.max], min=[image.min])})
        return image

    def get(self, field='image'):
        """Get imageinfo used on the field.

        Args:
            field (six.text_type): Defaults to 'image', Server defined field name,

        Returns:
            set[ImageInfo]: Image information.
        """

        select = self.select
        ret = set()
        for i in select[field]:
            try:
                data = json.loads(i)
                assert isinstance(data, dict)
                info = ImageInfo(max=data['max'][0],
                                 min=data['min'][0],
                                 path=data.get('path'))
                ret.add(info)
            except (TypeError, KeyError):
                continue
        return tuple(sorted(ret))
