# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations

from typing import Protocol
from .._row_id import RowID

class ViewService(Protocol):
    def refresh(self, database: str, module: str, module_type: str, /) -> None: ...
    def refresh_row(self, *id: RowID) -> None: ...
