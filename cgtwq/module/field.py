# -*- coding=UTF-8 -*-
"""Database module.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from wlf.decorators import deprecated

from ..model import FieldInfo
from .core import ModuleAttachment


class ModuleField(ModuleAttachment):
    """Field feature for module.  """

    def meta(self):
        """Get fields metadata in this module.

        Returns:
            tuple(FieldInfo)
        """

        resp = self.call(
            'c_field', 'get_join_module_data',
            field_array=FieldInfo.fields,
            order_field_array=["module", "sort_id"],
        )
        return tuple(FieldInfo(*i) for i in resp)

    def create(self, sign, type_, name=None, label=None):
        """Create new field in the module.

        Args:
            sign (str): Field sign
            type_ (str): Field type, see `core.FIELD_TYPES`.
            name (str, optional): Defaults to None. Field english name.
            label (str, optional): Defaults to None. Field chinese name.
        """

        module = self.module
        if '.' not in sign:
            module_name = 'task' if module.module_type == 'task' else module.name
            sign = '{}.{}'.format(module_name, sign)
        module.database.create_field(
            sign=sign, type_=type_, name=name, label=label)

    def delete(self, id_):
        """Delte field in the module.

        Args:
            id_ (str): Field id.
        """

        # Old api using: 'c_field', 'del_one_with_id',
        self.call(
            "v_main_window",
            "del_field_with_id",
            field_id=id_,
        )

    # Deprecated methods.
    # TODO: remove at next major version.

    def _format(self, name):
        """Formatted field name for this module.

        Args:
            name (text_type): Short field name.

        Returns:
            text_type: Full field name, for server.
        """

        module = self.module
        if ('.' in name
                or '#' in name):
            return name
        return '{}.{}'.format(module.default_field_namespace, name)

    format = deprecated(_format, 'Use `Field.in_namespace` instead.')
