# -*- coding=UTF-8 -*-
"""CGTeamWork style message, support image.  """

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import logging

import six
import cast_unknown as cast

from .server.web import upload_image
from .model import ImageInfo
from . import compat

LOGGER = logging.getLogger(__name__)

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import List, Union, Text, Any


class Message(six.text_type):
    """CGTeamWork style message, support image."""

    images = []  # type: List[Union[ImageInfo, Text]]

    def __new__(cls, obj):
        # type: (Any) -> Message
        ret = super(Message, cls).__new__(cls, obj)
        ret.images = []
        return ret

    def _check_images(self):
        # type: () -> List[ImageInfo]
        if any(not isinstance(i, ImageInfo) for i in self.images):
            raise ValueError(
                "Invalid images with the message, maybe not uploaded or wrong data format."
            )
        return self.images  # type: ignore

    def dumps(self):
        """Dump data to string in api version 5.2 defined format."""

        images = self._check_images()
        return json.dumps(
            {"data": self, "image": [i._asdict() for i in images]},  # type: ignore
        )

    def api_payload(self):
        # type: () -> Any
        """Dump data to in server defined format."""

        if compat.api_level() == compat.API_LEVEL_5_2:
            return self.dumps()
        images = self._check_images()
        return [{"type": "text", "content": self, "style": ""}] + [
            {
                "type": "image",
                "min": i.min,
                "max": i.max,
                "att_id": i.attachment_id,
            }
            for i in images
        ]

    def upload_images(self, folder, token):
        # type: (Text, Text) -> None
        """Upload contianed images to server. will replace items in `self.image`."""

        for index, img in enumerate(self.images):
            self.images[index] = _upload_image(img, folder, token)

    @classmethod
    def load(cls, data):
        # type: (Any) -> Message
        """Create message from data."""

        if isinstance(data, cls):
            return data


        data = data or ""

        try:
            data = json.loads(data)
            # api version 6.1
            if isinstance(data, list):
                list_data = data  # type: Any
                text = "\n<br>".join(i["content"] for i in list_data if i["type"] == "text")
                images = (
                    ImageInfo(max=i["max"], min=i["min"], attachment_id=i["att_id"])
                    for i in list_data
                    if i["type"] == "image"
                )
                ret = cls(text)
                ret.images = list(images)
                return ret
            assert isinstance(data, dict), type(data)
            text = data.get("data", "")
            images = data.get("image", data.get("images", []))
        except ValueError:
            text = data
            images = []

        ret = cls(text)
        ret.images = [ImageInfo(**i) for i in images]
        assert isinstance(ret, Message)
        return ret


def _upload_image(image, folder, token):
    # type: (Any, Text, Text) -> ImageInfo
    if isinstance(image, ImageInfo):
        return image
    if isinstance(image, dict):
        if image.get("max") and image.get("min"):
            return ImageInfo(
                max=image["max"],
                min=image["min"],
                path=image.get("path"),
                attachment_id=image.get("att_id"),
            )
        if image.get("path"):
            image = image["path"]
        else:
            raise TypeError(
                "ImageInfo takes dictionary that has key (max, min, path?).",
                image.keys(),
            )

    if not isinstance(image, (six.text_type, str)):
        raise TypeError("Not support such data type.", type(image))

    return upload_image(cast.text(image), folder, token)
