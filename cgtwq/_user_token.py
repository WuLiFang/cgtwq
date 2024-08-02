# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text


import time


class UserToken:
    def __init__(self, user_id, raw, expires_at=0):
        # type: (Text, Text, float) -> None

        self.user_id = user_id
        self.raw = raw
        self.expires_at = expires_at or time.time() + 16 * 60

    def expired(self):
        return time.time() >= self.expires_at
