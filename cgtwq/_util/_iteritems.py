# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Mapping, TypeVar, ItemsView

    TKey = TypeVar("TKey")
    TValue = TypeVar("TValue")


from ._compat import PY2


def iteritems(d):
    # type: (Mapping[TKey, TValue]) -> ItemsView[TKey, TValue]
    if PY2:
        return d.iteritems()  # type: ignore
    return d.items()
