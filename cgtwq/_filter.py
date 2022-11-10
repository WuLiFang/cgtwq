# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Text, Optional, List


class Filter:
    def __init__(self, left, op, right):
        # type: (Text, Text, Any) -> None
        self._left = left
        self._op = op
        self._right = right
        self._chain_to = None  # type: Optional[Filter]
        self._chain_logic = ""

    @property
    def left(self):
        return self._left

    @property
    def op(self):
        return self._op

    @property
    def right(self):
        return self._right

    @property
    def chain_to(self):
        return self._chain_to

    @property
    def chain_logic(self):
        return self._chain_logic

    def copy(self):
        v = Filter(self.left, self.op, self.right)
        v._chain_logic = self._chain_logic
        if self.chain_to:
            v._chain_to = self.chain_to.copy()
        return v

    def chain(self, logic, other):
        # type: (str, Filter) -> Filter
        v = self.copy()
        last = v
        while last._chain_to:
            last = last._chain_to
        last._chain_logic = logic
        last._chain_to = other
        return v

    def and_(self, other):
        # type: (Filter) -> Filter
        return self.chain("and", other)

    def or_(self, other):
        # type: (Filter) -> Filter
        return self.chain("or", other)

    def as_payload(self):
        # type: () -> List[Any]
        chain = []
        if self.chain_logic and self.chain_to:
            chain = [self.chain_logic] + self.chain_to.as_payload()
        return [[self.left, self.op, self.right]] + chain


NULL_FILTER = Filter("#id", "has", "%")
