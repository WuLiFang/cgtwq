# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import logging
import os

from six import text_type

from ..server.file import upload
from ..server.filetools import file_md5, genreate_thumb
from ..filter import Field, Filter
from ..model import (FileBoxDetail, ImageInfo, NoteInfo)
from ..resultset import ResultSet

_OS = {'windows': 'win', 'linux': 'linux', 'darwin': 'mac'}.get(
    __import__('platform').system().lower())  # Server defined os string.
LOGGER = logging.getLogger(__name__)

from .base import BaseSelection


class NoteMixin(BaseSelection):

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
