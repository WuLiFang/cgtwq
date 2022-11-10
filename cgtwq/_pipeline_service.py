# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Dict, Any
    from ._pipeline_service_protocol import PipelineService
    from ._compat_service import CompatService
    from ._http_client import HTTPClient
    from ._table_view_protocol import TableView

from ._filter import NULL_FILTER, Filter
from ._pipeline_table_view import PipelineTableView
from ._row_id import RowID


class PipelineServiceImpl:
    def __init__(self, http, compat):
        # type: (HTTPClient, CompatService) -> None
        self._http = http
        self._compat = compat

    def table(self, database, filter_by=NULL_FILTER):
        # type: (Text, Filter) -> TableView
        return PipelineTableView(
            self._http,
            self._compat,
            database,
            filter_by,
        )

    def neighbor_task(self, id):
        # type: (RowID) -> NeighborTaskResult
        resp = self._http.call(
            "c_pipeline_template",
            "get_next_and_previous_task",
            db=id.database,
            module=id.module,
            task_id=id.value,
        )
        data = resp.json()

        return NeighborTaskResult(id.database, id.module, data)


def _(v):
    # type: (PipelineServiceImpl) -> PipelineService
    return v


class NeighborTaskResult:
    def __init__(self, database, module, raw):
        # type: (Text,Text,Dict[Text,Any]) -> None
        self._database = database
        self._module = module
        self.raw = raw

    def next(self):
        return [
            RowID(self._database, self._module, "task", i) for i in self.raw["next"]
        ]

    def previous(self):
        return [
            RowID(self._database, self._module, "task", i) for i in self.raw["previous"]
        ]
