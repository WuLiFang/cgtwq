# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import uuid

import six
from deprecated import deprecated

from .. import account, compat, constants, exceptions
from ..filter import Field
from ..message import Message
from .core import SelectionAttachment
import cast_unknown as cast

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Iterable, List, Optional, Sequence, Text, Tuple, Union, Iterator

    from ..model import ImageInfo

import shutil


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
        # exists_ok not avaliable in python2.7
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


def _cast_strings(v):
    # type: (Sequence[Text]) -> Sequence[Text]
    if isinstance(v, six.binary_type):
        return (cast.text(v),)
    if isinstance(v, six.text_type):
        return (v,)
    return v


class SelectionFlow(SelectionAttachment):
    """Flow operation on selection."""

    def _update_v5_2(self, field, status, message="", images=()):
        # type: (Text, Text, Text, Tuple[Union[Text, ImageInfo], ...]) -> None
        select = self.select
        message = Message.load(message)
        message.images += images
        field = Field(field).in_namespace(self.select.module.default_field_namespace)

        try:
            self.call(
                "c_work_flow",
                "python_update_flow",
                field_sign=field,
                status=status,
                text=message.dumps(),
                task_id=select[0],
            )
        except ValueError as ex:
            if ex.args and ex.args[0] == (
                "work_flow::python_update_flow, " "no permission to qc"
            ):
                raise exceptions.PermissionError
            raise

    def _update_v6_1(self, field, status, message="", images=()):
        # type: (Text, Text, Text, Tuple[Union[Text, ImageInfo], ...]) -> None
        select = self.select
        message = Message.load(message)
        message.images += images
        field = Field(field).in_namespace(self.select.module.default_field_namespace)

        try:
            self.call(
                "c_work_flow",
                "python_update_flow",
                field_sign=field,
                status=status,
                dom_text_array=message.api_payload(),
                task_id=select[0],
            )
        except ValueError as ex:
            if ex.args and ex.args[0] == (
                "work_flow::python_update_flow, " "no permission to qc"
            ):
                raise exceptions.PermissionError
            raise

    def update(self, field, status, message="", images=()):
        # type: (Text, Text, Text, Tuple[Union[Text, ImageInfo], ...]) -> None
        """Update flow status."""
        # TODO: refactor arguments at next major version.
        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._update_v5_2(field, status, message, images)
        return self._update_v6_1(field, status, message, images)

    def _submit_v5_2(self, filenames, message, account_id):
        # type: (Sequence[Text], Union[Message, Text], Optional[Text]) -> None
        select = self.select
        message = Message.load(message)
        account_id = account_id or account.get_account_id(select.token)

        # Create path data.
        path_data = {"path": filenames, "file_path": filenames}
        select.call(
            "c_work_flow",
            "submit",
            task_id=select[0],
            account_id=account_id,
            version_id=self.create_version(filenames),
            submit_file_path_array=path_data,
            text=message.dumps(),
        )

    def _submit_v6_1(self, filenames, message, os, sign):
        # type: (Sequence[Text], Union[Message, Text], Text, Text) -> None
        select = self.select
        message = Message.load(message)

        version_id = self._create_version_v6_1(filenames, sign, os)
        select.call(
            "c_work_flow",
            "submit",
            task_id=select[0],
            submit_type=sign,
            dom_text_array=message.api_payload(),
            version_id=version_id,
        )

    def submit(
        self, filenames=(), message="", account_id=None, os=constants.OS, sign="review"
    ):
        # type: (Sequence[Text], Union[Message, Text], Optional[Text], Text, Text) -> None
        """Submit file to task, then change status to `Check`.

        Args:
            filenames (tuple, optional): Defaults to (). Local filenames.
            message (Message, optional): Defaults to "". Submit note(and images).
        """

        filenames = _cast_strings(filenames)
        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._submit_v5_2(filenames, message, account_id)
        return self._submit_v6_1(filenames, message, os, sign)

    def _create_version_v5_2(self, filenames, sign):
        # type: (Sequence[Text], Text) -> Text
        select = self.select
        version_id = uuid.uuid4().hex
        select.call(
            "c_version",
            "create",
            field_data_array={
                "#link_id": select[0],
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

    def _create_version_v6_1(self, filenames, sign, os):
        # type: (Sequence[Text], Text, Text) -> Text
        select = self.select
        filebox_data = select.filebox.get_submit(sign)
        submit_dir = filebox_data.path
        server_id = filebox_data.server_id
        filenames = tuple(_copy_to_dir(filenames, submit_dir) or _listdir(submit_dir))
        if not filenames:
            raise ValueError("no file to submit")
        version_id = select.call(
            "c_version",
            "client_create",
            link_id=select[0],
            sign=sign,
            submit_dir=submit_dir,
            submit_path_array=filenames,
            submit_file_path_array=filenames,
            server_id=server_id,
            os=os,
        )
        select.call(
            "c_file",
            "create",
            link_id=select[0],
            sign=sign,
            version_id=version_id,
            path_array=filenames,
            os=os,
            server_id=server_id,
        )
        return version_id

    def create_version(self, filenames, sign=None, version_id=None, os=constants.OS):
        # type: (Sequence[Text], Optional[Text] , Optional[Text], Text) -> Text
        """Create new task version.

        Args:
            filenames (list): Filename list.
            sign (str, optional): Defaults to None. Server version sign.
            version_id (str, optional): Deprecated. Defaults to None. Wanted version id.

        Returns:
            str: Created version id.
        """

        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._create_version_v5_2(filenames, sign or "Api Submit")
        return self._create_version_v6_1(filenames, sign or "review", os)

    def assign(self, accounts, start="", end=""):
        # type: (List[Text], Text, Text) -> None
        """Assgin tasks.

        Args:
            account (list): Account id list.
            start (str, optional): Defaults to ''. Task start date.
            end (str, optional): Defaults to ''. Task end date.
        """

        if isinstance(accounts, six.text_type):
            accounts = [accounts]
        select = self.select
        select.call(
            "c_work_flow",
            "assign_to",
            assign_account_id=",".join(accounts),
            start_date=start,
            end_date=end,
            task_id_array=select,
        )

    @deprecated(version="3.2.3", reason="Not avaliable in cgteamwork6.1")
    def has_field_permission(self, field):
        # type: (Text) -> bool
        """Return if current user has permission to edit the field."""
        if compat.api_level() != compat.API_LEVEL_5_2:
            raise NotImplementedError("not avaliable in cgteamwork 6.1")
        field = Field(field).in_namespace(self.select.module.default_field_namespace)
        resp = self.call(
            "c_work_flow",
            "is_status_field_has_permission",
            field_sign=field,
            task_id_array=self.select,
        )
        return resp

    def close(self, field, message="", images=()):
        # type: (Text, Text, Tuple[Union[Text, ImageInfo], ...]) -> None
        """Shorthand method to set take status to `Close`."""

        return self.update(field, "Close", message, images)

    def approve(self, field, message="", images=()):
        # type: (Text, Text, Tuple[Union[Text, ImageInfo], ...]) -> None
        """Shorthand method to set take status to `Approve`."""

        return self.update(field, "Approve", message, images)

    def retake(self, field, message="", images=()):
        # type: (Text, Text, Tuple[Union[Text, ImageInfo], ...]) -> None
        """Shorthand method to set take status to `Retake`."""

        return self.update(field, "Retake", message, images)

    def _list_submit_file_v5_2(self):
        # type: () -> Sequence[Text]
        raw_files = self.select.get_fields("task.submit_file_path").column(
            "task.submit_file_path"
        )
        return [j for i in raw_files for j in json.loads(i)["path"]]

    def _list_submit_file_v6_1(self, sign, os):
        # type: (Text,Text) -> Sequence[Text]
        s = self.select
        resp = s.module.database.call(
            "c_version",
            "get_submit_file",
            link_module=s.module.name,
            link_module_type=s.module.module_type,
            link_id_array=s,
            os=os,
            submit_type=sign,
        )
        return [j for i in resp for j in i["path"]]

    def list_submit_file(self, sign="review", os=constants.OS):
        # type: (Text, Text) -> Sequence[Text]
        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._list_submit_file_v5_2()
        return self._list_submit_file_v6_1(sign, os)
