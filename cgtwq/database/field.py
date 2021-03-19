# -*- coding=UTF-8 -*-
"""Database on cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..core import FIELD_TYPES, ControllerGetterMixin
from ..filter import Field, FilterList
from ..model import FieldMeta
from . import core

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Union, Tuple
    import cgtwq


class DatabaseField(core.DatabaseAttachment, ControllerGetterMixin):
    """Field feature for database.  """

    def filter(self, *args):
        # type: (Union[FilterList, cgtwq.Filter]) -> Tuple[FieldMeta, ...]
        r"""Get field metadata in the database.

        Args:
            \*filters (FilterList, Filter): Filters for server.

        Returns:
            tuple[FieldMeta]: Field information.
        """

        filters = (FilterList.from_arbitrary_args(*args)
                   or FilterList(Field('sign').has('%')))
        return self._filter_model(
            'c_field', 'get_with_filter', FieldMeta,
            filters=filters)

    def filter_one(self, *args):
        # type: (Union[FilterList, cgtwq.Filter]) -> FieldMeta
        """Get one field in the database.
            filters (Filter or FilterList): Filter.

        Returns:
            FieldMeta: Field information.
        """

        filters = FilterList.from_arbitrary_args(*args)
        resp = self.call(
            'c_field', 'get_one_with_filter',
            field_array=FieldMeta.fields,
            filter_array=filters
        )
        return FieldMeta(*resp)

    def create(self, sign, type_, name=None, label=None):
        # type: (Text, Text, Text, Text) -> None
        """Create new field in the module.

        Args:
            sign (str): Field sign
            type_ (str): Field type, see `core.FIELD_TYPES`.
            name (str, optional): Defaults to None. Field english name.
            label (str, optional): Defaults to None. Field chinese name.
        """

        assert type_ in FIELD_TYPES,\
            'Field type must in {}'.format(FIELD_TYPES)
        assert '.' in sign, 'Sign must contains a `.` character to specific module.'

        module, sign = sign.split('.')
        label = label or sign
        name = name or sign

        self.call(
            "c_field", "python_create",
            module=module,
            field_str=label,
            en_name=name,
            sign=sign,
            type=type_,
            field_name=sign,
        )

    def delete(self, id_):
        # type: (Text) -> None
        r"""Delete field in the module.

        Args:
            id_ (str): Field id.
        """

        self.call(
            'c_field', 'del_one_with_id',
            id=id_)
