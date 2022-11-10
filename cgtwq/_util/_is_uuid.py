# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text


from ._compat import text_type
from uuid import UUID


def is_uuid(text):
    # type: (Text) -> bool
    text = text_type(text)
    try:
        return text.lower() == text_type(UUID(text))
    except (TypeError, ValueError):
        return False
