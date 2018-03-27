# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..model import FileBoxDetail
from .base import BaseSelection, _OS


class FileboxMixin(BaseSelection):
    """Get filebox attached to the selection.   """

    def get_filebox(self, sign=None, id_=None):
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

        if not self:
            raise ValueError('Empty selection.')

        if id_:
            resp = self.call("c_file", "filebox_get_one_with_id",
                             task_id=self[0],
                             filebox_id=id_,
                             os=_OS)
        elif sign:
            resp = self.call("c_file", "filebox_get_one_with_sign",
                             task_id=self[0],
                             sign=sign,
                             os=_OS)
        else:
            raise ValueError(
                'Need at least one of (sign, id_) to get filebox.')

        if not resp.data:
            raise ValueError('No matched filebox.')
        assert isinstance(resp.data, dict), resp
        return FileBoxDetail(**resp.data)

    def get_filebox_submit(self):
        resp = self.call(
            'c_file', 'filebox_get_submit_data',
            task_id=self[0],
            os=_OS)
        return resp
