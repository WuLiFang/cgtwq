# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..filter import Filter
from .base import SelectionAttachment


class SelectionHistory(SelectionAttachment):
    """Get history of the selection.  """

    def get(self, filters=None):
        """Get selection related history.
            filters (Filter or FilterList, optional): Defaults to None.
                Addtional history filters.

        Returns:
            tuple[HistoryInfo]: History records.
        """

        select = self.select
        _filters = Filter('#task_id', select)
        if filters:
            _filters &= filters
        return select.module.get_history(_filters)

    def count(self, filters=None):
        """Count selection related history records.

        Args:
            filters (Filter or FilterList):
                Addtional history filters.

        Returns:
            int: Records count.
        """

        select = self.select
        _filters = Filter('#task_id', select)
        if filters:
            _filters &= filters
        return select.module.count_history(_filters)
