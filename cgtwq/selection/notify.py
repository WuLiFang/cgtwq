# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

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

    def add(self, text, account, images=()):
        """Add note to selected items.

        Args:
            text (str): Note text,support HTML.
            account (str): Account id.

        Raises:
            ValueError: When no item selected.
        """

        # TODO: Support image.

        select = self.select
        select.call("c_note", "create",
                    field_data_array={
                        "module": select.module.name,
                        "module_type": select.module.module_type,
                        "#task_id": ",".join(select),
                        "text": {'data': text, 'image': images},
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
