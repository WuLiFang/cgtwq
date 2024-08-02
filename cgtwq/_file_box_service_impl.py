# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text
    from ._file_box_service import FileBoxService
    from ._compat_service import CompatService
    from ._http_client import HTTPClient


# from ._fileBox_table_view import FileBoxTableView
from ._row_id import RowID
from ._file_box import FileBox
from . import constants


class FileBoxServiceImpl:
    def __init__(self, http, compat):
        # type: (HTTPClient, CompatService) -> None
        self._http = http
        self._compat = compat

    def get_by_sign(self, id, sign):
        # type: (RowID, Text) -> FileBox
        if self._compat.level <= self._compat.LEVEL_5_2:
            return self._get_by_sign_v5_2(id, sign)
        if self._compat.level <= self._compat.LEVEL_6_1:
            return self._get_by_sign_v6_1(id, sign)
        return self._get_by_sign_v7_0(id, sign)

    def _get_by_sign_v5_2(self, id, sign):
        # type: (RowID, Text) -> FileBox
        resp = self._http.call(
            "c_file",
            "filebox_get_one_with_sign",
            db=id.database,
            module=id.module,
            task_id=id.value,
            sign=sign,
            os=constants.OS,
        )
        return FileBox(resp.json())

    def _get_by_sign_v6_1(self, id, sign):
        # type: (RowID, Text) -> FileBox
        resp = self._http.call(
            "c_filebox",
            "filebox_get_one_with_sign",
            db=id.database,
            module=id.module,
            task_id=id.value,
            sign=sign,
            os=constants.OS,
        )
        return FileBox(resp.json())

    def _get_by_sign_v7_0(self, id, sign):
        # type: (RowID, Text) -> FileBox
        controller = "task"
        if id.module == "etask":
            controller = "etask"
        resp = self._http.call(
            controller,
            "get_sign_filebox",
            db=id.database,
            module=id.module,
            id=id.value,
            os=constants.OS,
            filebox_sign=sign,
        )
        return FileBox(resp.json())


def new_file_box_service(http, compat):
    # type: (HTTPClient, CompatService) -> FileBoxService
    return FileBoxServiceImpl(http, compat)
