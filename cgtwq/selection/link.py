# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .core import SelectionAttachment


class SelectionLink(SelectionAttachment):
    """Link feature for selection.  """

    def link(self, *id_list):
        """Link the selection to other items. """

        select = self.select
        select.call(
            "c_link", "set_link_id",
            id_array=self, link_id_array=id_list)

    def unlink(self, *id_list):
        """Unlink the selection with other items.  """

        select = self.select
        for id_ in select:
            select.call(
                "c_link", "remove_link_id",
                id=id_, link_id_array=id_list)

    def get(self):
        """Get linked items for the selections.

        Returns:
            set: All linked item id.
        """

        select = self.select
        ret = set()
        for id_ in select:
            resp = select.call("c_link", "get_link_id", id=id_)
            ret.add(resp)
        return ret
