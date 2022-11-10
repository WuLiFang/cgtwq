# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations

from typing import Protocol

from ._filter import Filter
from ._pipeline_service import NeighborTaskResult
from ._row_id import RowID
from ._table_view_protocol import TableView

class PipelineService(Protocol):
    def table(
        self,
        database: str,
        /,
        *,
        filter_by: Filter = ...,
    ) -> TableView: ...
    def neighbor_task(self, id: RowID) -> NeighborTaskResult: ...
