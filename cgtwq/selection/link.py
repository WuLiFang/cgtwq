# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import absolute_import, division, print_function, unicode_literals

from .core import SelectionAttachment
from deprecated import deprecated

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Set, Any


class SelectionLink(SelectionAttachment):
    """Link feature for selection."""

    def add(self, *id_list, **kwargs):
        # type: (Text, Any) -> None
        """Link the selection to other items."""
        to_module = kwargs.get("to_module", "asset")

        select = self.select
        select.call(
            "c_many2many",
            "add_link",
            module_tab_id_array=select,
            link_module_tab_id_array=id_list,
            link_module=to_module,
            is_main="Y",
        )

    link = deprecated(version="3.4.1", reason="renamed to `add`")(add)

    def remove(self, *id_list, **kwargs):
        # type: (Text, Any) -> None
        """Unlink the selection with other items."""
        to_module = kwargs.get("to_module", "asset")

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

    unlink = deprecated(version="3.4.1", reason="renamed to `remove`")(remove)

    def get(self, **kwargs):
        # type: (Any) -> Set[Text]
        """Get linked items for the selections.

        Returns:
            set: All linked item id.
        """
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
