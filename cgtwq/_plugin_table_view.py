# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Iterator, Sequence
    from ._compat_service import CompatService
    from ._http_client import HTTPClient
    from ._table_view_protocol import TableView

from ._row_id import RowID

from ._filter import Filter


class PluginTableView:
    def __init__(
        self,
        http,
        compat,
        filter_by,
    ):
        # type: (HTTPClient, CompatService, Filter) -> None
        self._http = http
        self._compat = compat
        self._filter_by = filter_by

    def __iter__(self):
        for (id,) in self.rows("#id"):
            yield RowID("", "", "", id)

    def rows(self, *fields):
        # type: (Text) -> Iterator[Sequence[Text]]
        resp = self._http.call(
            "c_plugin",
            "get_with_filter",
            field_array=[self._compat.transform_field(i) for i in fields],
            filter_array=self._compat.transform_filter(self._filter_by),
        )
        return resp.json()

    def column(self, field):
        # type: (Text) -> ...
        for (i,) in self.rows(field):
            yield i


def _(v):
    # type: (PluginTableView) -> TableView
    return v
