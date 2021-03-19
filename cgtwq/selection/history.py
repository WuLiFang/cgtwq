# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..filter import Filter
from .core import SelectionAttachment


TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Union, Tuple
    import cgtwq
    import cgtwq.model


class SelectionHistory(SelectionAttachment):
    """Get history of the selection.  """

    def _combine_filters(self, filters):
        # type: (Union[Filter, cgtwq.FilterList, None]) -> Union[cgtwq.FilterList, Filter]
        _filters = Filter('#task_id', self.select)
        if filters:
            _filters &= filters
        return _filters

    def get(self, filters=None):
        # type: (Union[Filter, cgtwq.FilterList, None]) -> Tuple[cgtwq.model.HistoryInfo, ...]
        """Get selection related history.
            Sorted by time, older first.

        Args:
            filters (Filter or FilterList, optional): Defaults to None.
                Additional history filters.

        Returns:
            tuple[HistoryInfo]: History records.
        """

        return tuple(sorted(
            self.select.module.history.filter(self._combine_filters(filters)),
            key=lambda i: i.time))

    def count(self, filters=None):
        # type: (Union[Filter, cgtwq.FilterList, None]) -> int
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
        # type: (cgtwq.model.HistoryInfo) -> None
        """Short hand method for `Module.undo_history`

        Args:
            history (HistoryInfo): History information.
        """

        return self.select.module.history.undo(history)
