# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import absolute_import, division, print_function, unicode_literals

from .core import SelectionAttachment
from deprecated import deprecated
from .. import compat

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Set, Any


class SelectionLink(SelectionAttachment):
    """Link feature for selection."""

    def _add_v5_2(self, *id_list, **kwargs):
        # type: (Text, Any) -> None
        to_module = kwargs["to_module"]

        select = self.select
        select.call(
            "c_many2many",
            "add_link",
            module_tab_id_array=select,
            link_module_tab_id_array=id_list,
            link_module=to_module,
            is_main="Y",
        )

    def _add_v6_1(self, *id_list, **kwargs):
        # type: (Text, Any) -> None
        to_module = kwargs["to_module"]

        select = self.select
        count_dict = {}
        for i in id_list:
            count_dict[i] = count_dict.setdefault(i, 0) + 1
        select.call(
            "c_many",
            "add_link",
            module_tab_id_array=select,
            link_module=to_module,
            link_module_id_data_array=count_dict,
        )

    def add(self, *id_list, **kwargs):
        # type: (Text, Any) -> None
        """Link the selection to other items."""
        to_module = kwargs.get("to_module", "asset")
        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._add_v5_2(*id_list, to_module=to_module)
        return self._add_v6_1(*id_list, to_module=to_module)

    link = deprecated(version="3.4.1", reason="renamed to `add`")(add)

    def _remove_v5_2(self, *id_list, **kwargs):
        # type: (Text, Any) -> None
        to_module = kwargs["to_module"]

        select = self.select
        for id_ in select:
            select.call(
                "c_many2many",
                "remove_link",
                id=id_,
                module_tab_id_array=select,
                link_module_tab_id_array=id_list,
                link_module=to_module,
                is_main="Y",
            )

    def _remove_v6_1(self, *id_list, **kwargs):
        # type: (Text, Any) -> None
        to_module = kwargs["to_module"]

        select = self.select
        for id_ in select:
            select.call(
                "c_many",
                "remove_link",
                id=id_,
                module_tab_id_array=select,
                link_module=to_module,
                link_module_tab_id_array=id_list,
            )

    def remove(self, *id_list, **kwargs):
        # type: (Text, Any) -> None
        """Unlink the selection with other items."""
        to_module = kwargs.get("to_module", "asset")
        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._remove_v5_2(*id_list, to_module=to_module)
        return self._remove_v6_1(*id_list, to_module=to_module)

    unlink = deprecated(version="3.4.1", reason="renamed to `remove`")(remove)

    def _get_v5_1(self, **kwargs):
        # type: (Any) -> Set[Text]
        to_module = kwargs.get("to_module", "asset")

        select = self.select
        ret = set()
        for id_ in select:
            resp = select.call(
                "c_many2many",
                "get_link",
                module_tab_id=id_,
                link_module=to_module,
                is_main="Y",
            )
            ret.update(resp)
        return ret

    def _get_v6_1(self, **kwargs):
        # type: (Any) -> Set[Text]
        to_module = kwargs.get("to_module", "asset")

        select = self.select
        ret = set()
        for id_ in select:
            resp = select.call(
                "c_many",
                "get_link",
                module_tab_id=id_,
                link_module=to_module,
            )
            ret.update(resp)
        return ret

    def get(self, **kwargs):
        # type: (Any) -> Set[Text]
        """Get linked items for the selections.

        Returns:
            set: All linked item id.
        """
        to_module = kwargs.get("to_module", "asset")
        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._get_v5_1(to_module=to_module)
        return self._get_v6_1(to_module=to_module)
