# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Any, Sequence
    from ._table_view import TableView
    from ._client import Client

import os

from ._compat_service import CompatService
from ._filter import NULL_FILTER, Filter
from ._flow_service_impl import new_flow_service
from ._row_id import RowID
from ._http_client import HTTPClient
from ._user_token import UserToken
from ._orm_table_view import ORMTableView
from ._pipeline_service_impl import new_pipeline_service
from ._file_box_service_impl import new_file_box_service
from ._image_service_impl import new_image_service
from ._util import iteritems


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
        pipeline = new_pipeline_service(http, compat)
        flow = new_flow_service(http, compat)
        file_box = new_file_box_service(http, compat)
        image = new_image_service(http, compat)

        self._http = http
        self._compat = compat
        self.file_box = file_box
        self.pipeline = pipeline
        self.flow = flow
        self.image = image

    @property
    def http_url(self):
        return self._http.url

    @property
    def token(self):
        return self._http.token

    @token.setter
    def token(self, v):
        # type: (UserToken) -> None
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

    def set(self, id, data):
        # type: (Sequence[RowID], dict[str, Any]) -> None

        if not id or not data:
            return
        data = {self._compat.transform_field(k): v for k, v in data.items()}

        if self._compat.level < self._compat.LEVEL_7_0:
            return self._set_v5_2(id, data)
        return self._set_v7_0(id, data)

    def _set_v5_2(self, id, data):
        # type: (Sequence[RowID], dict[str, Any]) -> None

        groups = {}  # type: dict[tuple[Text, Text,Text], list[Text]]
        for i in id:
            groups.setdefault((i.database, i.module, i.module_type), []).append(i.value)

        for key, id_list in iteritems(groups):
            database, module, module_type = key
            self._http.call(
                "c_orm",
                "set_in_id",
                db=database,
                module=module,
                module_type=module_type,
                id_array=id_list,
                sign_data_array=data,
            ).json()

    def _set_v7_0(self, id, data):
        # type: (Sequence[RowID], dict[str, Any]) -> None
        groups = {}  # type: dict[tuple[Text, Text,Text], list[Text]]
        for i in id:
            groups.setdefault((i.database, i.module, i.module_type), []).append(i.value)

        for key, id_list in iteritems(groups):
            database, module, module_type = key
            self._http.call(
                module_type,
                "set",
                db=database,
                module=module,
                module_type=module_type,
                id_array=id_list,
                sign_data_array=data,
                exec_event_filter=True,
            ).json()


def new_client(http_url="", version=""):
    # type: (Text, Text) -> Client
    return ClientImpl(http_url, version)
