# -*- coding=UTF-8 -*-
"""Database module.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..core import ControllerGetterMixin
from ..filter import FilterList
from ..model import HistoryInfo
from .core import ModuleAttachment


class ModuleHistory(ModuleAttachment, ControllerGetterMixin):
    """History feature for module.  """

    def filter(self, *filters):
        """Filter history record from the module.
            filters (Filter or FilterList): History filters.

        Returns:
            tuple[HistoryInfo]: History records.
        """

        filters = FilterList.from_arbitrary_args(*filters)
        return self._filter_model(
            "c_history", "get_with_filter",
            HistoryInfo, filters
        )

    def count(self, *filters):
        """Count history records in the module.

        Args:
            *filters (Filter or FilterList):
                History filters.

        Returns:
            int: Records count.
        """

        filters = FilterList.from_arbitrary_args(*filters)
        resp = self.call(
            "c_history", "count_with_filter",
            filter_array=FilterList(filters))
        return int(resp)

    def undo(self, history):
        """Undo a history.

        Args:
            history (HistoryInfo): History information.
        """
        assert isinstance(history, HistoryInfo), type(history)

        self.call(
            'v_history', "undo_data",
            id=history.id,
            task_id=history.task_id,
            show_field_sign_arr=[],
        )
