# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .base import BaseSelection


class LinkMixin(BaseSelection):
    """Link feature for selection.  """

    def link(self, *id_list):
        """Link the selection to other items. """

        self.call(
            "c_link", "set_link_id",
            id_array=self, link_id_array=id_list)

    def unlink(self, *id_list):
        """Unlink the selection with other items.  """

        for id_ in self:
            self.call(
                "c_link", "remove_link_id",
                id=id_, link_id_array=id_list)

    def get_linked(self):
        """Get linked items for the selections.

        Returns:
            set: All linked item id.
        """

        ret = set()
        for id_ in self:
            resp = self.call("c_link", "get_link_id", id=id_)
            ret.add(resp)
        return ret
