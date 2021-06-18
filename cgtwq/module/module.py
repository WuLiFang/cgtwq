# -*- coding=UTF-8 -*-
"""Database module.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

from deprecated import deprecated
import six

from ..core import ControllerGetterMixin
from ..filter import Field, Filter, FilterList
from ..model import FlowInfo
from ..selection import Selection
from .field import ModuleField
from .history import ModuleHistory

LOGGER = logging.getLogger(__name__)

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Text, Union, Tuple, Dict
    import cgtwq
    import cgtwq.model


@six.python_2_unicode_compatible
class Module(ControllerGetterMixin):
    """Module(Database table) in database.    """

    default_field_namespace = 'task'

    def __init__(self, name, database, module_type='task'):
        # type: (Text, cgtwq.Database, Text) -> None
        """
        Args:
            name (text_type): Server defined module name.
            database (Database): Parent database.
        """

        if name:
            self.name = name
        from ..database import Database
        assert isinstance(database, Database)
        self.database = database
        self.module_type = module_type
        self.label = None
        self._token = None

        # Attachment.
        self.field = ModuleField(self)
        self.history = ModuleHistory(self)

    def __getitem__(self, name):
        # type: (Text) -> Selection
        if isinstance(name, (Filter, FilterList)):
            return self.filter(name)
        return self.select(name)

    def __str__(self):
        return ('Module<database={0.database.name}, '
                'name={0.name}, type={0.module_type}, '
                'label={0.label}>').format(self)

    @property
    def token(self):
        # type: () -> Text
        """User token.   """
        return self._token or self.database.token

    @token.setter
    def token(self, value):
        # type: (Text) -> None
        self._token = value

    def call(self, *args, **kwargs):
        # type: (Any, *Any) -> Any
        """Call on this module.   """

        kwargs.setdefault('token', self.token)
        kwargs.setdefault('module', self.name)
        kwargs.setdefault('module_type', self.module_type)
        return self.database.call(*args, **kwargs)

    def select(self, *id_list):
        # type: (Text) -> Selection
        r"""Create selection on this module.

        Args:
            \*id_list (text_type): Id list to select.

        Returns:
            Selection: Created selection.
        """

        return Selection(self, *id_list)

    def filter(self, *args, **kwargs):
        # type: (Union[FilterList, Filter], *Any) -> Selection
        r"""Create selection with filter on this module.

        Args:
            \*filters (FilterList, Filter): Filters for server.
            \*\*kwargs:

        \*\*kwargs:
            namespace (str, optional): Default field namespace.

        Returns:
            Selection: Created selection.
        """

        namespace = kwargs.pop('namespace', self.default_field_namespace)
        filters = FilterList.from_arbitrary_args(
            *args).in_namespace(namespace)

        resp = self.call('c_orm', 'get_with_filter',
                         sign_array=(Field('id').in_namespace(self.name),),
                         sign_filter_array=filters)
        if resp:
            id_list = [i[0] for i in resp]
        else:
            id_list = []
        return Selection(self, *id_list)

    def distinct(self, *args, **kwargs):
        # type: (Union[cgtwq.FilterList, cgtwq.Filter], *Any) -> Tuple[Any, ...]
        r"""Get distinct value in the module.

        Args:
            \*filters (FilterList, Filter): Filters for server.
            \*\*kwargs:

        \*\*kwargs:
            key: Distinct key, defaults to field of first filter.
            namespace (str, optional): Default field namespace.

        Returns:
            tuple
        """

        namespace = kwargs.pop('namespace', self.default_field_namespace)
        filters = FilterList.from_arbitrary_args(
            *args).in_namespace(namespace)
        key = Field(kwargs.pop('key', filters[0][0])).in_namespace(namespace)

        resp = self.call(
            'c_orm', 'get_distinct_with_filter',
            distinct_sign=key,
            sign_filter_array=filters,
            order_sign_array=[key],
        )
        assert all(len(i) == 1 for i in resp), 'Unknown response'
        return tuple(i[0] for i in resp)

    def create(self, kwargs=None, **data):
        # type: (Dict[Text, Any], *Any) -> None
        r"""Create entry from data.

        Args:
            kwargs (dict):
            \*\*data[str, Any]: Data to create a entry.

        \*\*data:
            namespace (str, optional): Default field namespace.
        """

        kwargs = kwargs or dict()
        namespace = kwargs.pop('namespace', self.default_field_namespace)

        data = {
            Field(k).in_namespace(namespace): v
            for k, v in data.items()}
        self.call('c_orm', 'create',
                  sign_data_array=data)

    def count(self, *args, **kwargs):
        # type: (Union[cgtwq.FilterList, cgtwq.Filter], *Any) -> int
        r"""Count matched entity in database.

        Args:
            \\*filters (FilterList, Filter): Filters for server.
            \*\*kwargs:
                namespace (str, optional): Default field namespace.

        Returns:
            int: Count value.
        """

        namespace = kwargs.pop('namespace', self.default_field_namespace)
        filters = FilterList.from_arbitrary_args(
            *args).in_namespace(namespace)

        resp = self.call('c_orm', 'get_count_with_filter',
                         sign_filter_array=filters)
        return int(resp)

    def pipelines(self):
        """All pipeline in this module.

        Returns:
            tuple[Pipeline]: namedtuple for ('id', 'name', 'module').
        """

        return self.database.pipeline.filter(Filter('module', self.name))

    def flow(self):
        """Workflow of the module.  """

        resp = self.call('c_flow', 'get_data')
        return tuple(FlowInfo(*i) for i in resp)

    @deprecated(
        version='3.0.0',
        reason='Use `Module.field.meta` insted.',
    )
    def fields(self):
        """Get fields in this module.  """

        return self.field.meta()

    @deprecated(
        version='3.0.0',
        reason='Use `Module.field.format` insted.',
    )
    def format_field(self, name):
        # type: (Text) -> Text
        """Formatted field name for this module.

        Args:
            name (text_type): Short field name.

        Returns:
            text_type: Full field name, for server.
        """

        return self.field.format(name)

    @deprecated(
        version='3.0.0',
        reason='Use `Module.field.create` insted.',
    )
    def create_field(self, sign, type_, name=None, label=None):
        # type: (Text, Text, Text, Text) -> None
        r"""Create new field in the module.

        Args:
            sign (str): Field sign
            type_ (str): Field type, see `core.FIELD_TYPES`.
            name (str, optional): Defaults to None. Field english name.
            label (str, optional): Defaults to None. Field chinese name.
        """
        return self.field.create(sign, type_, name, label)

    @deprecated(
        version='3.0.0',
        reason='Use `Module.field.delete` insted.',
    )
    def delete_field(self, id_):
        # type: (Text) -> None
        r"""Delete field in the module.

        Args:
            id_ (str): Field id.
        """

        self.field.delete(id_)

    @deprecated(
        version='3.0.0',
        reason='Use `Module.history.filter` insted.',
    )
    def get_history(self, filters):
        # type: (Union[cgtwq.Filter, cgtwq.FilterList]) -> Tuple[cgtwq.model.HistoryInfo, ...]
        """Get history record from the module.
            filters (Filter or FilterList): History filters.

        Returns:
            tuple[HistoryInfo]: History records.
        """

        return self.history.filter(filters)

    @deprecated(
        version='3.0.0',
        reason='Use `Module.history.count` insted.',
    )
    def count_history(self, filters):
        # type: (Union[cgtwq.Filter, cgtwq.FilterList]) -> int
        """Count history records in the module.

        Args:
            filters (Filter or FilterList):
                History filters.

        Returns:
            int: Records count.
        """

        return self.history.count(filters)

    @deprecated(
        version='3.0.0',
        reason='Use `Module.history.undo` insted.',
    )
    def undo_history(self, history):
        # type: (cgtwq.model.HistoryInfo) -> None
        """Undo a history.

        Args:
            history (HistoryInfo): History information.
        """

        self.history.undo(history)

    @deprecated(
        version='3.0.0',
        reason='Use `FilterList.in_namespace` insted.',
    )
    def format_filters(self, filters):
        # type: (Union[FilterList, Filter]) -> FilterList
        """Format field name in filters.

        Args:
            filters (FilterList, Filter): Format target.

        Returns:
            FilterList: Formatted filters.
        """

        assert isinstance(filters, (Filter, FilterList)), type(filters)
        ret = FilterList(filters)
        for i in ret:
            if isinstance(i, Filter):
                i[0] = self.format_field(i[0])
        return ret
