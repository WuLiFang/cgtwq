# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Sequence, Iterator, Iterable
    from ._flow_service import FlowService
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

    def submit(
        self,
        id,
        filenames,
        msg="",
    ):
        # type: (RowID, Sequence[Text], MessageInput) -> None
        pass

    def _get_submit_file_box_v5_2(self, id):
        # type: (RowID) -> FileBox
        resp = self._http.call(
            "c_file",
            "filebox_get_submit_data",
            db=id.database,
            module=id.module,
            task_id=id.value,
            os=constants.OS,
        )
        return FileBox(resp.json())

    def _get_submit_file_box_v6_1(self, id, sign):
        # type: (RowID,Text) -> FileBox
        resp = self._http.call(
            "c_filebox",
            "filebox_get_submit_data",
            db=id.database,
            module=id.module,
            task_id=id.value,
            os=constants.OS,
            sign=sign,
        )
        return FileBox(resp.json())

    def _get_first_submit_file_box_v7_0(self, id):
        # type: (RowID) -> FileBox
        # spell-checker: word filebox etask
        controller = "task"
        if id.module == "etask":
            controller = "etask"
        sign_list = self._http.call(
            controller,
            "get_submit_filebox_sign",
            db=id.database,
            module=id.module,
            id=id.value,
        ).json()  # type: list[str]
        if not sign_list:
            raise ValueError("submission file box not found")
        resp = self._http.call(
            controller,
            "get_sign_filebox",
            db=id.database,
            module=id.module,
            id=id.value,
            os=constants.OS,
            filebox_sign=sign_list[0],
        )
        return FileBox(resp.json())

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
        file_box = self._get_submit_file_box_v6_1(id, sign)
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

    def _create_version_v7_0(self, id, filenames):
        # type: (RowID,Sequence[Text]) -> Text
        file_box = self._get_first_submit_file_box_v7_0(id)
        submit_dir = file_box.path
        server_id = file_box.server_id
        filenames = tuple(_copy_to_dir(filenames, submit_dir) or _listdir(submit_dir))
        if not filenames:
            raise ValueError("no file to submit")
        version_id = self._http.call(
            "version",
            "client_create",
            link_id=id.value,
            sign=file_box.sign,
            submit_dir=submit_dir,
            submit_path_array=filenames,
            submit_file_path_array=filenames,
            server_id=server_id,
            os=os,
        ).json()
        self._http.call(
            "file",
            "create",
            link_id=id.value,
            sign=file_box.sign,
            version_id=version_id,
            path_array=filenames,
            os=os,
            server_id=server_id,
        )
        return version_id

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

    def _submit_v5_2(
        self,
        id,
        filenames,
        msg="",
    ):
        # type: (RowID, Sequence[Text], MessageInput) -> None
        msg = Message.from_input(msg)
        path_data = {"path": filenames, "file_path": filenames}
        self._http.call(
            "c_work_flow",
            "submit",
            db=id.database,
            module=id.module,
            module_type=id.module_type,
            task_id=id.value,
            account_id=self._http.token.user_id,
            version_id=self._create_version_v5_2(id, filenames, "Api Submit"),
            submit_file_path_array=path_data,
            text=msg.as_payload_v5_2(),
        )

    def _submit_v6_1(
        self,
        id,
        filenames,
        msg="",
    ):
        # type: (RowID, Sequence[Text], MessageInput) -> None
        msg = Message.from_input(msg)
        version_id = self._create_version_v6_1(id, filenames, "review", constants.OS)
        self._http.call(
            "c_work_flow",
            "submit",
            db=id.database,
            module=id.module,
            module_type=id.module_type,
            task_id=id.value,
            submit_type="review",
            dom_text_array=msg.as_payload_v6_1(),
            version_id=version_id,
        )

    def _submit_v7_0(
        self,
        id,
        filenames,
        msg="",
    ):
        # type: (RowID, Sequence[Text], MessageInput) -> None
        msg = Message.from_input(msg)

        version_id = self._create_version_v7_0(id, filenames)
        self._http.call(
            "work_flow",
            "submit",
            db=id.database,
            module=id.module,
            module_type=id.module_type,
            task_id=id.value,
            dom_text_array=msg.as_payload_v6_1(),
            version_id=version_id,
        )


def new_flow_service(http, compat):
    # type: (HTTPClient, CompatService) -> FlowService
    return FlowServiceImpl(http, compat)
