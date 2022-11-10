# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Sequence, Union, Any


from ._image import Image
from ._util import cast_text
import json


class Message:
    @classmethod
    def from_input(cls, input):
        # type: (MessageInput) -> Message
        if isinstance(input, cls):
            return input
        return cls(cast_text(input))

    def __init__(self, html="", images=()):
        # type: (Text, Sequence[Image]) ->None
        self.html = html
        self.images = images

    def as_payload_v5_2(self):
        # type: () -> Text
        return json.dumps(
            dict(data=self.html, images=[i.as_payload_v5_2() for i in self.images])
        )

    def as_payload_v6_1(self):
        # type: () -> list[dict[Text, Any]]
        return [dict(type="text", content=self.html, style="")] + [
            i.as_payload_v6_1() for i in self.images
        ]


if TYPE_CHECKING:
    MessageInput = Union[Text, Message]
else:
    MessageInput = None
