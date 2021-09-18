# -*- coding=UTF-8 -*-
"""Database module.  """
from __future__ import absolute_import, division, print_function, unicode_literals

from deprecated import deprecated

from ..model import FieldMeta
from .core import ModuleAttachment

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Tuple


class ModuleField(ModuleAttachment):
    """Field feature for module."""

    def meta(self):
        # type: () -> Tuple[FieldMeta, ...]
        """Get fields metadata in this module.

        Returns:
            tuple(FieldMeta)
        """

        resp = self.call(
            "c_field",
            "get_join_module_data",
            field_array=FieldMeta.fields,
            order_field_array=["module", "sort_id"],
        )
        return tuple(FieldMeta(*i) for i in resp)

    def create(self, sign, type_, name=None, label=None):
        # type: (Text, Text, Text, Text) -> None
        """Create new field in the module.

        Args:
            sign (str): Field sign
            type_ (str): Field type, see `core.FIELD_TYPES`.
            name (str, optional): Defaults to None. Field english name.
            label (str, optional): Defaults to None. Field chinese name.
        """

        module = self.module
        if "." not in sign:
            module_name = "task" if module.module_type == "task" else module.name
            sign = "{}.{}".format(module_name, sign)
        module.database.create_field(sign=sign, type_=type_, name=name, label=label)

    def delete(self, id_):
        # type: (Text) -> None
        r"""Delete field in the module.

        Args:
            id_ (str): Field id.
        """

        # Old api using: 'c_field', 'del_one_with_id',
        self.call(
            "v_main_window",
            "del_field_with_id",
            field_id=id_,
        )

    @deprecated(
        version="3.0.0",
        reason="Use `Field.in_namespace` instead.",
    )
    def format(self, name):
        # type: (Text) -> Text
        """Formatted field name for this module.

        Args:
            name (text_type): Short field name.

        Returns:
            text_type: Full field name, for server.
        """

        module = self.module
        if "." in name or "#" in name:
            return name
        return "{}.{}".format(module.default_field_namespace, name)
