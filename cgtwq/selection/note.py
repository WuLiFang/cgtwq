# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..model import NoteInfo
from .base import BaseSelection


class NoteMixin(BaseSelection):
    """Note on the Selection.  """

    def get_notes(self):
        """Get notes on first item in the selection.

        Raises:
            ValueError: When no item selected.

        Returns:
            tuple[NoteInfo]: namedtuple about note information.
        """

        if not self:
            raise ValueError('Empty selection.')

        resp = self.call("c_note", "get_with_task_id",
                         task_id=self[0],
                         field_array=NoteInfo.fields)
        return tuple(NoteInfo(*i) for i in resp.data)

    def add_note(self, text, account):
        """Add note to selected items.

        Args:
            text (str): Note text,support HTML.
            account (str): Account id.

        Raises:
            ValueError: When no item selected.
        """

        if not self:
            raise ValueError('Empty selection.')

        self.call("c_note", "create",
                  field_data_array={
                      "module": self.module.name,
                      "#task_id": ",".join(self),
                      "text": text,
                      "#from_account_id": account})
