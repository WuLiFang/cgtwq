# -*- coding=UTF-8 -*-
"""Database module.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..core import ControllerGetterMixin
from ..filter import FilterList
from ..model import HistoryInfo
from .core import ModuleAttachment
TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Tuple, Union
    import cgtwq


class ModuleHistory(ModuleAttachment, ControllerGetterMixin):
    """History feature for module.  """

    def filter(self, *args):
        # type: (Union[cgtwq.Filter, cgtwq.FilterList]) -> Tuple[HistoryInfo, ...]
        """Filter history record from the module.
            filters (Filter or FilterList): History filters.

        Returns:
            tuple[HistoryInfo]: History records.
        """

        filters = FilterList.from_arbitrary_args(*args)
        return self._filter_model(
            "c_history", "get_with_filter",
            HistoryInfo, filters
        )

    def count(self, *args):
        # type: (Union[cgtwq.Filter, cgtwq.FilterList]) -> int
        """Count history records in the module.

        Args:
            *filters (Filter or FilterList):
                History filters.

        Returns:
            int: Records count.
        """

        filters = FilterList.from_arbitrary_args(*args)
        resp = self.call(
            "c_history", "count_with_filter",
            filter_array=FilterList(filters))
        return int(resp)

    def undo(self, history):
        # type: (HistoryInfo) -> None
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
