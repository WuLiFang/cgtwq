# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Iterator, Sequence
    from ._table_view_protocol import TableView

from ._filter import Filter, NULL_FILTER
from ._http_client import HTTPClient
from ._row_id import RowID

from ._compat_service import CompatService


class ORMTableView:
    page_size = 1000

    def __init__(
        self,
        http,
        compat,
        database,
        module,
        module_type,
        filter_by,
    ):
        # type: (HTTPClient, CompatService, Text, Text, Text, Filter) -> None
        self._http = http
        self._compat = compat
        self._database = database
        self._module = module
        self._module_type = module_type
        self._id_field = "%s.id" % (self._module_type)
        if filter_by is NULL_FILTER:
            filter_by = Filter(self._id_field, "has", "%")
        self._filter_by = filter_by

    def __iter__(self):
        for id in self.column(self._id_field):
            yield RowID(self._database, self._module, self._module_type, id)

    def rows(self, *fields):
        # type: (Text) -> Iterator[Sequence[Text]]
        page_size = self.page_size
        page_index = 0
        has_next_page = True
        sign_array = [self._compat.transform_field(i) for i in fields]
        sign_filter_array = self._compat.transform_filter(self._filter_by)
        while has_next_page:
            has_next_page = False
            resp = self._http.call(
                "c_orm",
                "get_with_filter",
                db=self._database,
                module=self._module,
                module_type=self._module_type,
                sign_array=sign_array,
                order_sign_array=sign_array[:3],
                sign_filter_array=sign_filter_array,
                limit="%d" % (page_size,),
                start_num="%d" % (page_index * page_size,),
            )
            for index, i in enumerate(resp.json()):
                if index == page_size - 1:
                    has_next_page = True
                yield i
            page_index += 1

    def column(self, field):
        # type: (Text) -> ...
        for (i,) in self.rows(field):
            yield i


def _(v):
    # type: (ORMTableView) -> TableView
    return v
