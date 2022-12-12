# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Any, Sequence


from six import python_2_unicode_compatible  # type: ignore
from ._util import cast_text
from ._filter import Filter


@python_2_unicode_compatible
class FieldSign:
    def __init__(self, s):
        # type: (Text) -> None
        self._s = s

    def __str__(self):
        return cast_text("FieldSign<%s>" % (self._s,))

    @property
    def value(self):
        return self._s

    def equal(self, v):
        # type: (Any) -> Filter
        return Filter(self._s, "=", v)

    def equal_ignore_case(self, v):
        # type: (Any) -> Filter
        return Filter(self._s, "~", v)

    def not_equal(self, v):
        # type: (Any) -> Filter
        return Filter(self._s, "!=", v)

    def less_than(self, v):
        # type: (Any) -> Filter
        return Filter(self._s, "<", v)

    def less_equal_than(self, v):
        # type: (Any) -> Filter
        return Filter(self._s, "<=", v)

    def greater_than(self, v):
        # type: (Any) -> Filter
        return Filter(self._s, ">", v)

    def greater_equal_than(self, v):
        # type: (Any) -> Filter
        return Filter(self._s, ">=", v)

    def like(self, v):
        # type: (Text) -> Filter
        """
        - `%` match zero or many character.
        - `-` match one character
        """
        return Filter(self._s, "concat", v)

    def not_like(self, v):
        # type: (Text) -> Filter
        "same syntax as `like`"
        return Filter(self._s, "!concat", v)

    def has(self, v):
        # type: (Text) -> Filter
        return Filter(self._s, "has", v)

    def not_has(self, v):
        # type: (Text) -> Filter
        return Filter(self._s, "!has", v)

    def has_ignore_case(self, v):
        # type: (Text) -> Filter
        return Filter(self._s, "~has", v)

    def in_(self, v):
        # type: (Sequence[Text]) -> Filter
        return Filter(self._s, "in", v)

    def starts_with(self, v):
        # type: (Text) -> Filter
        return Filter(self._s, "start", v)

    def ends_with(self, v):
        # type: (Text) -> Filter
        return Filter(self._s, "end", v)

    def is_(self, v):
        # type: (Any) -> Filter
        "unknown usage"
        return Filter(self._s, "is", v)
