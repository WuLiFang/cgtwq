# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text


class Image:
    def __init__(self, max, min, attachment_id):
        # type: (Text, Text, Text) -> None
        self.max = max
        self.min = min
        self.attachment_id = attachment_id

    def as_payload_v5_2(self):
        d = dict(max=self.max, min=self.min)
        if self.attachment_id:
            d["attachment_id"] = self.attachment_id
        return d

    def as_payload_v6_1(self):
        d = dict(type="image", max=self.max, min=self.min)
        if self.attachment_id:
            d["attachment_id"] = self.attachment_id
        return d
