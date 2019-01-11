# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..filter import Filter
from .core import SelectionAttachment


class SelectionHistory(SelectionAttachment):
    """Get history of the selection.  """

    def _combine_filters(self, filters):
        _filters = Filter('#task_id', self.select)
        if filters:
            _filters &= filters
        return _filters

    def get(self, filters=None):
        """Get selection related history.
            Sorted by time, older first.

        Args:
            filters (Filter or FilterList, optional): Defaults to None.
                Additional history filters.

        Returns:
            tuple[HistoryInfo]: History records.
        """

        return sorted(
            self.select.module.history.filter(self._combine_filters(filters)),
            key=lambda i: i.time)

    def count(self, filters=None):
        """Count selection related history records.

        Args:
            filters (Filter or FilterList):
                Additional history filters.

        Returns:
            int: Records count.
        """

        return self.select.module.history.count(
            self._combine_filters(filters))

    def undo(self, history):
        """Short hand method for `Module.undo_history`

        Args:
            history (HistoryInfo): History information.
        """

        return self.select.module.history.undo(history)
