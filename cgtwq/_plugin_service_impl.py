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
import json


# spell-checker: word argvs


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
        if self._compat.level < self._compat.LEVEL_7_0:
            return self._get_5_2(id)
        return self._get_7_0(id)

    def _get_5_2(self, id):
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

    def _get_7_0(self, id):
        # type: (Text) -> ...
        assert id, "id is required"
        resp = self._http.call(
            "plugin",
            "get_argvs",
            id=id,
        )
        data = resp.json()
        return Plugin(id, "unknown", "unknown", json.dumps(data))

    def save(self, obj, only_fields=()):
        # type: (Plugin, Iterable[Text]) -> None
        if self._compat.level < self._compat.LEVEL_7_0:
            return self._save_5_2(obj, only_fields)
        return self._save_7_0(obj)

    def _save_5_2(self, obj, only_fields=()):
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
        self._http.call(
            "c_plugin",
            "set_one_with_id",
            id=obj.id,
            field_data_array=data,
        )

    def _save_7_0(self, obj):
        # type: (Plugin) -> None
        self._http.call(
            "plugin",
            "set_argvs",
            id=obj.id,
            argv_data={k: v.value for k, v in obj.argv()},
        )


def new_plugin_service(http, compat):
    # type: (HTTPClient, CompatService) -> PluginService
    return PluginServiceImpl(http, compat)
