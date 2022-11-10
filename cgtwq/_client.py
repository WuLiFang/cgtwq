# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text
    from ._table_view_protocol import TableView
    from ._client_protocol import Client
    from ._pipeline_service_protocol import PipelineService
    from ._flow_service_protocol import FlowService

import os

from ._compat_service import CompatService
from ._filter import NULL_FILTER, Filter
from ._flow_service import FlowServiceImpl
from ._http_client import HTTPClient
from ._orm_table_view import ORMTableView
from ._pipeline_service import PipelineServiceImpl


class ClientImpl(object):
    default_http_url = os.getenv("CGTEAMWORK_URL", "http://192.168.55.11")
    default_version = os.getenv("CGTEAMWORK_VERSION", "")

    def __init__(self, http_url="", version=""):
        # type: (Text, Text) -> None
        http = HTTPClient(http_url or self.default_http_url)
        compat = CompatService(
            CompatService.level_from_version(version or self.default_version)
            or CompatService.level_from_http(http),
        )
        pipeline = PipelineServiceImpl(
            http,
            compat,
        )
        flow = FlowServiceImpl(
            http,
            compat,
        )

        self._http = http
        self._compat = compat
        self.pipeline = pipeline  # type: PipelineService
        self.flow = flow  # type: FlowService

    @property
    def http_url(self):
        return self._http.url

    @property
    def token(self):
        return self._http.token

    @token.setter
    def token(self, v):
        # type: (Text) -> None
        self._http.token = v

    def table(self, database, module, module_type, filter_by=NULL_FILTER):
        # type: (Text, Text, Text, Filter) -> TableView
        return ORMTableView(
            self._http,
            self._compat,
            database,
            module,
            module_type,
            filter_by,
        )


def _(v):
    # type: (ClientImpl) -> Client
    return v
