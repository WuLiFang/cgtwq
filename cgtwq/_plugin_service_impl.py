# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Iterable
    from ._plugin_service import PluginService
    from ._compat_service import CompatService
    from ._http_client import HTTPClient
    from ._table_view import TableView

from ._filter import NULL_FILTER, Filter
from ._plugin import Plugin
from ._plugin_table_view import PluginTableView
from ._util import iteritems


class PluginServiceImpl(object):
    def __init__(self, http, compat):
        # type: (HTTPClient, CompatService) -> None
        self._http = http
        self._compat = compat

    def table(self, filter_by=NULL_FILTER):
        # type: (Filter) -> TableView
        return PluginTableView(
            self._http,
            self._compat,
            filter_by,
        )

    def find(self, filter_by=NULL_FILTER):
        # type: (Filter) -> ...
        for id, name, type, raw_argv in self.table(filter_by).rows(
            "#id", "name", "type", "argv"
        ):
            yield Plugin(id, name, type, raw_argv)

    def get(self, id):
        # type: (Text) -> ...
        assert id, "id is required"
        resp = self._http.call(
            "c_plugin",
            "get_one_with_id",
            id=id,
            field_array=["name", "type", "argv"],
        )
        name, type, raw_argv = resp.json()
        return Plugin(id, name, type, raw_argv)

    def save(self, obj, only_fields=()):
        # type: (Plugin, Iterable[Text]) -> None
        data = dict(
            type=obj.type,
            name=obj.name,
            argv=obj.raw_argv,
        )
        fields = list(data.keys())
        only_fields = set(only_fields)
        if only_fields:
            data = {k: v for k, v in iteritems(data) if k in only_fields}
        if not data:
            raise ValueError("only_fields item should be one of (%s)", fields)
        resp = self._http.call(
            "c_plugin",
            "set_one_with_id",
            id=obj.id,
            field_data_array=data,
        )
        resp.json()


def new_plugin_service(http, compat):
    # type: (HTTPClient, CompatService) -> PluginService
    return PluginServiceImpl(http, compat)
