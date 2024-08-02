# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Iterator, Sequence
    from ._compat_service import CompatService
    from ._http_client import HTTPClient
    from ._table_view import TableView

from ._row_id import RowID

from ._filter import Filter


class PipelineTableView:
    def __init__(
        self,
        http,
        compat,
        database,
        filter_by,
    ):
        # type: (HTTPClient, CompatService,  Text, Filter) -> None
        self._http = http
        self._compat = compat
        self._database = database
        self._filter_by = filter_by

    def __iter__(self):
        for id, module, module_type in self.rows("#id", "module", "module_type"):
            yield RowID(self._database, module, module_type, id)

    def rows(self, *fields):
        # type: (Text) -> Iterator[Sequence[Text]]
        if self._compat.level < self._compat.LEVEL_7_0:
            return self._rows_v5_2(*fields)
        return self._rows_v7_0(*fields)

    def column(self, field):
        # type: (Text) -> ...
        for (i,) in self.rows(field):
            yield i

    def _rows_v5_2(self, *fields):
        # type: (Text) -> Iterator[Sequence[Text]]
        resp = self._http.call(
            "c_pipeline",
            "get_with_filter",
            db=self._database,
            field_array=[self._compat.transform_field(i) for i in fields],
            filter_array=self._compat.transform_filter(self._filter_by),
        )
        return resp.json()

    def _rows_v7_0(self, *fields):
        # type: (Text) -> Iterator[Sequence[Text]]
        resp = self._http.call(
            "pipeline",
            "get_filter",
            db=self._database,
            field_array=[self._compat.transform_field(i) for i in fields],
            filter_array=self._compat.transform_filter(self._filter_by),
        )
        return resp.json()


def _(v):
    # type: (PipelineTableView) -> TableView
    return v
