# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations

from typing import Any, List

class Filter:
    left: str
    op: str
    right: Any
    chain_to: Filter
    chain_logic: str
    def __init__(self, left: str, op: str, right: Any, /) -> None: ...
    def chain(self, logic: str, other: Filter) -> Filter: ...
    def and_(self, other: Filter) -> Filter: ...
    def or_(self, other: Filter) -> Filter: ...
    def as_payload(self) -> List[Any]: ...

NULL_FILTER: Filter
