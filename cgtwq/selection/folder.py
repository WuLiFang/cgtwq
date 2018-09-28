# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .core import _OS, SelectionAttachment


class SelectionFolder(SelectionAttachment):
    """Folder feature for selection.  """

    def from_sign(self, *sign_list):

        select = self.select

        resp = select.call(
            "c_folder", "get_replace_path_in_sign",
            sign_array=sign_list,
            os=_OS)

        assert isinstance(resp, dict), type(resp)
        return resp

    def all(self):
        """All related folder path.

        Returns:
            list[str]: Folder path list.
        """

        return self.call(
            'c_folder', 'get_create_folder_data',
            os=_OS)
