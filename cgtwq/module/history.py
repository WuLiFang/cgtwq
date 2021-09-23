# -*- coding=UTF-8 -*-
"""Database module.  """
from __future__ import absolute_import, division, print_function, unicode_literals

from ..core import ControllerGetterMixin
from ..filter import FilterList
from ..model import HistoryInfo
from .core import ModuleAttachment
from .. import compat

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Tuple, Union
    import cgtwq


class ModuleHistory(ModuleAttachment, ControllerGetterMixin):
    """History feature for module."""

    def _filter_v5_2(self, *args):
        # type: (Union[cgtwq.Filter, cgtwq.FilterList]) -> Tuple[HistoryInfo, ...]

        filters = FilterList.from_arbitrary_args(*args)
        fields = (
            "#id",
            "#task_id",
            "#account_id",
            "step",
            "status",
            "file",
            "text",
            "create_by",
            "time",
        )
        resp = self.call(
            "c_history",
            "get_with_filter",
            field_array=fields,
            filter_array=filters,
        )
        return tuple(HistoryInfo(*i) for i in resp)

    def _filter_v6_1(self, *args):
        # type: (Union[cgtwq.Filter, cgtwq.FilterList]) -> Tuple[HistoryInfo, ...]

        filters = FilterList.from_arbitrary_args(*args)
        fields = (
            "#id",
            "#link_id",
            "account_id",
            "step",
            "status",
            "file",
            "text",
            "create_by",
            "time",
        )
        resp = self.call(
            "c_history",
            "get_with_filter",
            field_array=fields,
            filter_array=filters,
        )
        return tuple(HistoryInfo(*i) for i in resp)

    def filter(self, *args):
        # type: (Union[cgtwq.Filter, cgtwq.FilterList]) -> Tuple[HistoryInfo, ...]
        """Filter history record from the module.
            filters (Filter or FilterList): History filters.

        Returns:
            tuple[HistoryInfo]: History records.
        """

        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._filter_v5_2(*args)
        return self._filter_v6_1(*args)

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
            "c_history", "count_with_filter", filter_array=FilterList(filters)
        )
        return int(resp)

    def _undo_v5_2(self, history):
        # type: (HistoryInfo) -> None
        assert isinstance(history, HistoryInfo), type(history)

        self.call(
            "v_history",
            "undo_data",
            id=history.id,
            task_id=history.task_id,
            show_field_sign_arr=[],
        )

    def _undo_v6_1(self, history):
        # type: (HistoryInfo) -> None
        assert isinstance(history, HistoryInfo), type(history)

        self.call(
            "v_history",
            "undo",
            id=history.id,
            main_id=history.task_id,
            show_sign_arr=[],
        )

    def undo(self, history):
        # type: (HistoryInfo) -> None
        """Undo a history.

        Args:
            history (HistoryInfo): History information.
        """
        assert isinstance(history, HistoryInfo), type(history)

        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._undo_v5_2(history)
        return self._undo_v6_1(history)
