# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..filter import Filter
from .base import BaseSelection


class HistoryMixin(BaseSelection):
    """Get history of the selection.  """

    def get_history(self, filters=None):
        """Get selection related history.
            filters (Filter or FilterList, optional): Defaults to None.
                Addtional history filters.

        Returns:
            tuple[HistoryInfo]: History records.
        """

        _filters = Filter('#task_id', self)
        if filters:
            _filters &= filters
        return self.module.get_history(_filters)

    def count_history(self, filters=None):
        """Count selection related history records.

        Args:
            filters (Filter or FilterList):
                Addtional history filters.

        Returns:
            int: Records count.
        """

        _filters = Filter('#task_id', self)
        if filters:
            _filters &= filters
        return self.module.count_history(_filters)
