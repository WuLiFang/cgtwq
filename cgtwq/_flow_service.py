# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Sequence, Optional, Iterator, Iterable
    from ._flow_service_protocol import FlowService
    from ._compat_service import CompatService
    from ._http_client import HTTPClient
    from ._row_id import RowID

import os
import shutil
from uuid import uuid4

from . import constants, exceptions
from ._file_box import FileBox
from ._message import Message, MessageInput


def _listdir(path):
    # type: (Text) -> Iterator[Text]
    try:
        for i in os.listdir(path):
            yield os.path.join(path, i)
    except OSError:
        return


def _is_under_dir(filename, dir):
    # type: (Text, Text) -> bool
    return os.path.normcase(os.path.abspath(filename)).startswith(
        os.path.normcase(os.path.abspath(dir))
    )


def _copy_to_dir(filenames, dir):
    # type: (Iterable[Text], Text) -> Iterator[Text]
    try:
        # exists_ok not available in python2.7
        os.makedirs(dir)
    except OSError:
        pass
    for src in filenames:
        if _is_under_dir(src, dir):
            yield src
            continue
        dst = os.path.join(dir, os.path.basename(src))
        try:
            shutil.copy(src, dst)
        except shutil.SameFileError:
            pass
        yield dst


class FlowServiceImpl:
    def __init__(self, http, compat):
        # type: (HTTPClient, CompatService) -> None
        self._http = http
        self._compat = compat

    def _get_submit_v5_2(self, id):
        # type: (RowID) -> FileBox
        resp = self._http.call(
            "c_file",
            "filebox_get_submit_data",
            database=id.database,
            module=id.module,
            task_id=id.value,
            os=constants.OS,
        )
        return FileBox(resp.json())

    def _get_submit_v6_1(self, id, sign):
        # type: (RowID,Text) -> FileBox
        resp = self._http.call(
            "c_filebox",
            "filebox_get_submit_data",
            database=id.database,
            module=id.module,
            task_id=id.value,
            os=constants.OS,
            sign=sign,
        )
        return FileBox(resp.json())

    def get_submit(self, id, sign="review"):
        # type: (RowID,Text) -> FileBox
        compat = self._compat
        if compat.level == compat.LEVEL_5_2:
            return self._get_submit_v5_2(id)
        return self._get_submit_v6_1(id, sign)

    def _create_version_v5_2(
        self,
        id,
        filenames,
        sign,
    ):
        # type: (RowID, Sequence[Text], Text) -> Text
        version_id = uuid4().hex
        self._http.call(
            "c_version",
            "create",
            field_data_array={
                "#link_id": id.value,
                "version": "",
                "filename": [os.path.basename(i) for i in filenames],
                "local_path": filenames,
                "web_path": [],
                "sign": sign,
                "image": "",
                "from_version": "",
                "is_upload_web": "N",
                "#id": version_id,
            },
        )
        return version_id

    def _create_version_v6_1(self, id, filenames, sign, os):
        # type: (RowID,Sequence[Text], Text, Text) -> Text
        file_box = self.get_submit(id, sign)
        submit_dir = file_box.path
        server_id = file_box.server_id
        filenames = tuple(_copy_to_dir(filenames, submit_dir) or _listdir(submit_dir))
        if not filenames:
            raise ValueError("no file to submit")
        version_id = self._http.call(
            "c_version",
            "client_create",
            link_id=id.value,
            sign=sign,
            submit_dir=submit_dir,
            submit_path_array=filenames,
            submit_file_path_array=filenames,
            server_id=server_id,
            os=os,
        ).json()
        self._http.call(
            "c_file",
            "create",
            link_id=id.value,
            sign=sign,
            version_id=version_id,
            path_array=filenames,
            os=os,
            server_id=server_id,
        )
        return version_id

    def create_version(self, id, filenames, sign=None, os=constants.OS):
        # type: (RowID, Sequence[Text], Optional[Text], Text) -> Text
        """Create new task version.

        Args:
            filenames (list): Filename list.
            sign (str, optional): Defaults to None. Server version sign.

        Returns:
            str: Created version id.
        """

        compat = self._compat
        if compat.level == compat.LEVEL_5_2:
            return self._create_version_v5_2(id, filenames, sign or "Api Submit")
        return self._create_version_v6_1(id, filenames, sign or "review", os)

    def _update_v5_2(
        self,
        id,
        field,
        status,
        msg,
    ):
        # type: (RowID, Text, Text, MessageInput) -> None
        message = Message.from_input(msg)

        try:
            self._http.call(
                "c_work_flow",
                "python_update_flow",
                db=id.database,
                module=id.module,
                module_type=id.module_type,
                task_id=id.value,
                field_sign=field,
                status=status,
                text=message.as_payload_v5_2(),
            ).json()
        except ValueError as ex:
            if ex.args and ex.args[0] == (
                "work_flow::python_update_flow, " "no permission to qc"
            ):
                raise exceptions.PermissionError
            raise

    def _update_v6_1(
        self,
        id,
        field,
        status,
        msg,
    ):
        # type: (RowID, Text, Text, MessageInput) -> None
        message = Message.from_input(msg)
        try:
            self._http.call(
                "c_work_flow",
                "python_update_flow",
                db=id.database,
                module=id.module,
                module_type=id.module_type,
                task_id=id.value,
                field_sign=field,
                status=status,
                dom_text_array=message.as_payload_v6_1(),
            ).json()
        except ValueError as ex:
            if ex.args and ex.args[0] == (
                "work_flow::python_update_flow, " "no permission to qc"
            ):
                raise exceptions.PermissionError
            raise

    def update(
        self,
        id,
        field,
        status,
        msg="",
    ):
        # type: (RowID, Text, Text, MessageInput) -> None
        if self._compat.level == self._compat.LEVEL_5_2:
            return self._update_v5_2(id, field, status, msg)
        return self._update_v6_1(id, field, status, msg)


def _(v):
    # type: (FlowServiceImpl) -> FlowService
    return v
