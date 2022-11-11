# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Text, Dict
    from ._plugin_service import PluginService

from .._util import is_uuid
import sys
from ._ws_client import WSClient
from ._plugin_context_result import PluginContextResult
from .._plugin_service_impl import PluginServiceImpl as BasePluginServiceImpl

from .._compat_service import CompatService
from .._http_client import HTTPClient


def _default_plugin_id():
    for i in sys.argv[1:]:
        if is_uuid(i):
            return i
    return ""


class PluginServiceImpl(BasePluginServiceImpl):
    def __init__(self, http, compat, ws):
        # type: ( HTTPClient, CompatService,WSClient) -> None
        super(PluginServiceImpl, self).__init__(http, compat)
        self.ws = ws
        self.default_plugin_id = _default_plugin_id()

    def context(self, id=""):
        # type: (Text) -> PluginContextResult
        plugin_uuid = id or self.default_plugin_id
        data = self.ws.call_main_widget("get_plugin_data", plugin_uuid=plugin_uuid)
        if not data or data is True:
            data = {}  # type: Dict[Text, Any]
        assert isinstance(data, dict), type(data)
        return PluginContextResult(data)

    def report_result(self, ok, id=""):
        # type: (bool, Text) -> None
        uuid = id or self.default_plugin_id
        self.ws.call_main_widget(
            "exec_plugin_result",
            uuid=uuid,
            result=ok,
            type="send",
        )


def new_plugin_service(http, compat, ws):
    # type: (HTTPClient, CompatService,WSClient) -> PluginService
    return PluginServiceImpl(http, compat, ws)
