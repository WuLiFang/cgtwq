# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..model import FileBoxInfo
from .base import SelectionAttachment, _OS


class SelectionFilebox(SelectionAttachment):
    """File operation on selection.  """

    def get(self, sign=None, id_=None):
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

        select = self.select

        if id_:
            resp = select.call("c_file", "filebox_get_one_with_id",
                               task_id=select[0],
                               filebox_id=id_,
                               os=_OS)
        elif sign:
            resp = select.call("c_file", "filebox_get_one_with_sign",
                               task_id=select[0],
                               sign=sign,
                               os=_OS)
        else:
            raise ValueError(
                'Need at least one of (sign, id_) to get filebox.')

        if not resp.data:
            raise ValueError('No matched filebox.')
        return FileBoxInfo(**resp.data)

    def get_submit(self):
        """Get filebox that set to submit.

        Returns:
            model.FileboxInfo: Filebox information.
        """

        select = self.select
        resp = select.call(
            'c_file', 'filebox_get_submit_data',
            task_id=select[0],
            os=_OS)
        assert isinstance(resp.data, dict), resp
        return FileBoxInfo(**resp.data)
