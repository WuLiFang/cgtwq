# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import absolute_import, division, print_function, unicode_literals

from deprecated import deprecated

from ..model import FileBoxInfo
from .core import SelectionAttachment
from .. import compat, constants

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text


class SelectionFilebox(SelectionAttachment):
    """File operation on selection."""

    def _from_id_v5_2(self, id_):
        # type: (Text) -> FileBoxInfo
        select = self.select
        resp = select.call(
            "c_file",
            "filebox_get_one_with_id",
            task_id=select[0],
            filebox_id=id_,
            os=constants.OS,
        )
        if not resp:
            raise ValueError("SelectionFilebox.from_id: no matched filebox", id_)
        return FileBoxInfo(**resp)

    def _from_id_v6_1(self, id_):
        # type: (Text) -> FileBoxInfo
        select = self.select
        resp = select.call(
            "c_filebox",
            "filebox_get_one_with_id",
            task_id=select[0],
            filebox_id=id_,
            os=constants.OS,
        )
        if not resp:
            raise ValueError("SelectionFilebox.from_id: no matched filebox", id_)
        return FileBoxInfo(**resp)

    def from_id(self, id_):
        # type: (Text) -> FileBoxInfo
        r"""Get filebox information from id.

        Args:
            id_ (str): Filebox id.

        Raises:
            ValueError: No matched filebox.

        Returns:
            FileboxInfo
        """
        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._from_id_v5_2(id_)
        return self._from_id_v6_1(id_)

    def _from_sign_v5_2(self, sign):
        # type: (Text) -> FileBoxInfo
        select = self.select
        resp = select.call(
            "c_file",
            "filebox_get_one_with_sign",
            task_id=select[0],
            sign=sign,
            os=constants.OS,
        )
        if not resp:
            raise ValueError("SelectionFilebox.from_sign: no matched filebox", sign)
        return FileBoxInfo(**resp)

    def _from_sign_v6_1(self, sign):
        # type: (Text) -> FileBoxInfo
        select = self.select
        resp = select.call(
            "c_filebox",
            "filebox_get_one_with_sign",
            task_id=select[0],
            sign=sign,
            os=constants.OS,
        )
        if not resp:
            raise ValueError("SelectionFilebox.from_sign: no matched filebox", sign)
        return FileBoxInfo(**resp)

    def from_sign(self, sign):
        # type: (Text) -> FileBoxInfo
        """Get filebox information from sign.

        Args:
            sign (str): Filebox sign.

        Raises:
            ValueError: No matched filebox.

        Returns:
            FileboxInfo
        """
        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._from_sign_v5_2(sign)
        return self._from_sign_v6_1(sign)

    def _get_submit_v5_2(self):
        # type: () -> FileBoxInfo
        select = self.select
        resp = select.call(
            "c_file", "filebox_get_submit_data", task_id=select[0], os=constants.OS
        )
        assert isinstance(resp, dict), resp
        return FileBoxInfo(**resp)

    def _get_submit_v6_1(self, sign):
        # type: (Text) -> FileBoxInfo
        select = self.select
        resp = select.call(
            "c_filebox",
            "filebox_get_submit_data",
            task_id=select[0],
            os=constants.OS,
            sign=sign,
        )
        assert isinstance(resp, dict), resp
        return FileBoxInfo(**resp)

    def get_submit(self, sign="review"):
        # type: (Text) -> FileBoxInfo
        """Get filebox that set to submit.
        Returns:
            model.FileboxInfo: Filebox information.
        """
        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._get_submit_v5_2()
        return self._get_submit_v6_1(sign)

    @deprecated(version="3.0.0", reason="Use `from_sign` or `from_id` instead.")
    def get(self, sign=None, id_=None):
        # type: (Text, Text) -> FileBoxInfo
        """Get one filebox with sign or id_.

        Args:
            sign (text_type): Server defined filebox sign.
            id_ (text_type): Server filebox id,
                if given, will ignore `sign` value.

        Raises:
            ValueError: When selection is empty.
            ValueError: When insufficient argument.
            ValueError: When got empty result.

        Returns:
            FileBoxInfo: Filebox information.
        """

        if id_:
            return self.from_id(id_)
        elif sign:
            return self.from_sign(sign)
        else:
            raise ValueError("Need at least one of (sign, id_) to get filebox.")
