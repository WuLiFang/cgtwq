# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations

from typing import Iterator, Sequence, Protocol

from ._row_id import RowID

class TableView(Protocol):
    def __iter__(self) -> Iterator[RowID]: ...
    def rows(self, *fields: str) -> Iterator[Sequence[str]]: ...
    def column(self, field: str) -> Iterator[str]: ...
