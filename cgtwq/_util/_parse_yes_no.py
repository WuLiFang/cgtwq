# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text


def parse_yes_no(v):
    # type: (Text) -> bool
    if v in ("Y", "y", "yes", "YES"):
        return True
    return False
