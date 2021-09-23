# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import absolute_import, division, print_function, unicode_literals

from ..account import get_account_id
from ..message import Message
from ..model import NoteInfo
from .core import SelectionAttachment
from .. import compat, filter

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Tuple, Union, Any
    import cgtwq.model


class SelectionNotify(SelectionAttachment):
    """Note or message on the Selection."""

    def _get_v5_2(self):

        select = self.select

        fields = (
            "#id",
            "#task_id",
            "#from_account_id",
            "text",
            "time",
            "create_by",
            "module",
        )
        resp = select.call(
            "c_note", "get_with_task_id", task_id=select[0], field_array=fields
        )
        return tuple(NoteInfo(*i) for i in resp)

    def _get_v6_1(self):

        select = self.select
        fields = (
            "#id",
            "#link_id",
            "from_account_id",
            "dom_text",
            "create_time",
            "create_by",
            "module",
        )
        ids = list(select)
        fl = filter.FilterList(filter.Field("#link_id").has(ids[0]))
        for i in ids[1:]:
            fl.append("or")
            fl.append(filter.Field("#link_id").has(i))

        resp = select.call(
            "c_note",
            "get_with_filter",
            filter_array=fl,
            field_array=fields,
        )
        return tuple(NoteInfo(*i) for i in resp)

    def get(self):
        """Get notes on first item in the selection.

        Returns:
            tuple[NoteInfo]: namedtuple about note information.
        """

        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._get_v5_2()
        return self._get_v6_1()

    def add(self, text, account=None, images=()):
        # type: (Text, Text, Tuple[Union[cgtwq.model.ImageInfo, Text,], ...]) -> ...
        """Add note to selected items.

        Args:
            text (str): Note text,support HTML.
            account (str): Account id.

        Raises:
            ValueError: When no item selected.
        """

        account = account or get_account_id(self.select.token)

        # TODO: Refactor arguments at next major version.
        message = Message.load(text)
        message.images += images

        text_key = "dom_text"
        id_key = "#link_id"
        from_account_id_key = "from_account_id"
        if compat.api_level() == compat.API_LEVEL_5_2:
            text_key = "text"
            id_key = "#task_id"
            from_account_id_key = "#from_account_id"

        select = self.select
        select.call(
            "c_note",
            "create",
            field_data_array={
                "module": select.module.name,
                "module_type": select.module.module_type,
                id_key: ",".join(select),
                text_key: message.api_payload(),
                from_account_id_key: account,
            },
        )

    def _send_v5_2(self, title, content, *to, **kwargs):
        # type: (Text, Text, Text, *Any) -> None
        select = self.select
        from_ = kwargs.get("from_")

        return select.call(
            "c_msg",
            "send_task",
            task_id=select[0],
            account_id_array=to,
            title=title,
            content=content,
            from_account_id=from_,
        )

    def _send_v6_1(self, title, content, *to, **kwargs):
        # type: (Text, Text, Text, *Any) -> None
        select = self.select

        return select.call(
            "c_msg",
            "send_task",
            task_id=select[0],
            account_id_array=to,
            content=[{"type": "text", "content": "<h1>%s</h1>%s" % (title, content)}],
        )

    def send(self, title, content, *to, **kwargs):
        # type: (Text, Text, Text, *Any) -> None
        r"""Send message to users.

        Args:
            title (text_type): Message title.
            content (text_type): Message content, support html.
            *to: Users that will recives message, use account_id.
            \*\*kwargs:
                from_: Unknown effect. used in `cgtw` module.
        """
        # pylint: disable=invalid-name

        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._send_v5_2(title, content, *to, **kwargs)
        return self._send_v6_1(title, content, *to, **kwargs)

    def _delete_v5_2(self, *note_id_list):
        # type: (Text) -> None

        self.call(
            "v_note",
            "del_in_id",
            id_array=note_id_list,
            task_id_array=self.select,
            show_sign_array=[],
        )

    def _delete_v6_1(self, *note_id_list):
        # type: (Text) -> None

        for i in note_id_list:
            self.call(
                "v_note",
                "delete",
                id=i,
                link_id=",".join(self.select),
            )

    def delete(self, *note_id_list):
        # type: (Text) -> None
        """Delete note on selection."""

        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._delete_v5_2(*note_id_list)
        return self._delete_v6_1(*note_id_list)
