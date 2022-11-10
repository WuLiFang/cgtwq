# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text

    from ._view_service_protocol import ViewService
    from ._ws_client import WSClient
    from .._compat_service import CompatService
    from .._row_id import RowID

from .._util import iteritems


class ViewServiceImpl:
    def __init__(self, ws, compat):
        # type: (WSClient, CompatService) -> None
        self._ws = ws
        self._compat = compat

    def _refresh_v5_2(self, database, module):
        # type: (Text, Text) -> None
        self._ws.call(
            "view_control",
            "refresh",
            type="send",
            database=database,
            module=module,
        )

    def _refresh_v6_1(self, database, module, module_type):
        # type: (Text, Text, Text) -> None
        self._ws.call(
            "http_server",
            "refresh_main",
            type="send",
            db=database,
            module=module,
            module_type=module_type,
        )

    def refresh(self, database, module, module_type):
        # type: (Text, Text, Text) -> None
        compat = self._compat
        if compat.level == compat.LEVEL_5_2:
            return self._refresh_v5_2(database, module)
        return self._refresh_v6_1(database, module, module_type)

    def refresh_row(self, *ids):
        # type: (RowID) -> None
        groups = {}  # type: dict[tuple[Text,Text,Text],set[RowID]]
        for i in ids:
            groups.setdefault((i.database, i.module, i.module_type), set()).add(i)
        compat = self._compat
        for k, v in iteritems(groups):
            database, module, module_type = k
            if compat.level == compat.LEVEL_5_2:
                self._refresh_v5_2(database, module)
            else:
                self._ws.call(
                    "http_server",
                    "refresh_main_recorder",
                    type="send",
                    db=database,
                    module=module,
                    module_type=module_type,
                    id_list=[i.value for i in v],
                )


def new_view_service(ws, compat):
    # type: (WSClient, CompatService) -> ViewService
    return ViewServiceImpl(ws, compat)
