# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations

from typing import Protocol, Sequence

from ._message import MessageInput
from ._row_id import RowID

class FlowService(Protocol):
    def update(
        self,
        id: RowID,
        field: str,
        status: str,
        msg: MessageInput = ...,
        /,
    ) -> None: ...
    def submit(
        self,
        id: RowID,
        filenames: Sequence[str],
        msg: MessageInput = ...,
        /,
    ) -> None: ...
