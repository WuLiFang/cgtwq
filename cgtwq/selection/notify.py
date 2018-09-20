# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..account import get_account_id
from ..message import Message
from ..model import NoteInfo
from .base import SelectionAttachment


class SelectionNotify(SelectionAttachment):
    """Note or message on the Selection.  """

    def get(self):
        """Get notes on first item in the selection.

        Returns:
            tuple[NoteInfo]: namedtuple about note information.
        """

        select = self.select
        resp = select.call("c_note", "get_with_task_id",
                           task_id=select[0],
                           field_array=NoteInfo.fields)
        return tuple(NoteInfo(*i) for i in resp)

    def add(self, text, account=None, images=()):
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

        select = self.select
        select.call("c_note", "create",
                    field_data_array={
                        "module": select.module.name,
                        "module_type": select.module.module_type,
                        "#task_id": ",".join(select),
                        "text": message.dumps(),
                        "#from_account_id": account})

    def send(self, title, content, *to, **kwargs):
        """Send message to users.

        Args:
            title (text_type): Message title.
            content (text_type): Message content, support html.
            *to: Users that will recives message, use account_id.
            **kwargs:
                from_: Unknown effect. used in `cgtw` module.
        """
        # pylint: disable=invalid-name

        select = self.select
        from_ = kwargs.get('from_')

        return select.call(
            'c_msg', 'send_task',
            task_id=select[0],
            account_id_array=to,
            title=title,
            content=content,
            from_account_id=from_
        )

    def delete(self, *note_id_list):
        """Delete note on selection.  """

        self.call(
            'v_note', 'del_in_id',
            id_array=note_id_list,
            task_id_array=self.select,
            show_sign_array=[],
        )
