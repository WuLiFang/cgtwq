# -*- coding=UTF-8 -*-
"""Database module.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

import six
from six import text_type
from six.moves import reduce

from wlf.decorators import deprecated

from ..core import ControllerGetterMixin
from ..filter import Field, Filter, FilterList
from ..model import FieldInfo, FlowInfo, HistoryInfo
from ..selection import Selection
from .field import ModuleField
from .history import ModuleHistory

LOGGER = logging.getLogger(__name__)


@six.python_2_unicode_compatible
class Module(ControllerGetterMixin):
    """Module(Database table) in database.    """

    default_field_namespace = 'task'

    def __init__(self, name, database, module_type='task'):
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
        if isinstance(name, (Filter, FilterList)):
            return self.filter(name)
        return self.select(name)

    def __str__(self):
        return ('Module<database={0.database.name}, '
                'name={0.name}, type={0.module_type}, '
                'label={0.label}>').format(self)

    @property
    def token(self):
        """User token.   """
        return self._token or self.database.token

    @token.setter
    def token(self, value):
        self._token = value

    def call(self, *args, **kwargs):
        """Call on this module.   """

        kwargs.setdefault('token', self.token)
        kwargs.setdefault('module', self.name)
        kwargs.setdefault('module_type', self.module_type)
        return self.database.call(*args, **kwargs)

    def select(self, *id_list):
        """Create selection on this module.

        Args:
            *id_list (text_type): Id list to select.

        Returns:
            Selection: Created selection.
        """

        return Selection(self, *id_list)

    def filter(self, *filters):
        """Create selection with filter on this module.

        Args:
            *filters (FilterList, Filter): Filters for server.

        Returns:
            Selection: Created selection.
        """

        filters = reduce(lambda a, b: a & b, filters)
        _filters = self.format_filters(filters)
        resp = self.call('c_orm', 'get_with_filter',
                         sign_array=(self.format_field('id'),),
                         sign_filter_array=_filters)
        if resp:
            id_list = [i[0] for i in resp]
        else:
            id_list = []
        return Selection(self, *id_list)

    def distinct(self, *filters, **kwargs):
        """Get distinct value in the module.

        Args:
            *filters (FilterList, Filter): Filters for server.
            **kwargs:
                key: Distinct key, defaults to field of first filter.

        Returns:
            tuple
        """

        filters = reduce(lambda a, b: a & b, filters)
        filters = self.format_filters(filters or Field('#id').has('%'))
        key = self.format_field(kwargs.pop('key', filters[0][0]))

        resp = self.call(
            'c_orm', 'get_distinct_with_filter',
            distinct_sign=key,
            sign_filter_array=filters,
            order_sign_array=[key],
        )
        assert all(len(i) == 1 for i in resp), 'Unknown response'
        return tuple(i[0] for i in resp)

    def create(self, **data):
        """Create entry from data.

        Args:
            **data[str, Any]: Data to create a entry.
        """

        self.call('c_orm', 'create',
                  sign_data_array=(self.format_field('id'),),
                  sign_filter_array={self.format_field(k): v for k, v in data.items()})

    def count(self, *filters):
        """Count matched entity in database.

        Returns:
            int: Count value.
        """

        filters = reduce(lambda a, b: a & b, filters)
        _filters = self.format_filters(filters)
        resp = self.call('c_orm', 'get_count_with_filter',
                         sign_filter_array=_filters)
        return int(resp)

    def format_filters(self, filters):
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

    def pipelines(self):
        """All pipeline in this module.

        Returns:
            tuple[Pipeline]: namedtuple for ('id', 'name', 'module').
        """

        return self.database.get_pipelines(Filter('module', self.name))

    def flow(self):
        """Workflow of the module.  """

        resp = self.call('c_flow', 'get_data')
        return tuple(FlowInfo(*i) for i in resp)

    # Deprecated methods.

    def _fields(self):
        """Get fields in this module.  """

        return self.field.meta()

    fields = deprecated(_fields, reason='Use `Module.field.meta` insted.')

    def _format_field(self, name):
        """Formatted field name for this module.

        Args:
            name (text_type): Short field name.

        Returns:
            text_type: Full field name, for server.
        """

        return self.field.format(name)

    format_field = deprecated(
        _format_field, reason='Use `Module.field.format` insted.')

    def _create_field(self, sign, type_, name=None, label=None):
        """Create new field in the module.

        Args:
            sign (str): Field sign
            type_ (str): Field type, see `core.FIELD_TYPES`.
            name (str, optional): Defaults to None. Field english name.
            label (str, optional): Defaults to None. Field chinese name.
        """
        return self.field.create(sign, type_, name, label)

    create_field = deprecated(
        _create_field, reason='Use `Module.field.create` insted.')

    def _delete_field(self, id_):
        """Delte field in the module.

        Args:
            id_ (str): Field id.
        """

        self.field.delete(id_)

    delete_field = deprecated(
        _delete_field, reason='Use `Module.field.delete` insted.')

    def _get_history(self, filters):
        """Get history record from the module.
            filters (Filter or FilterList): History filters.

        Returns:
            tuple[HistoryInfo]: History records.
        """

        return self.history.filter(filters)

    get_history = deprecated(
        _get_history, reason='Use `Module.history.filter` insted.')

    def _count_history(self, filters):
        """Count history records in the module.

        Args:
            filters (Filter or FilterList):
                History filters.

        Returns:
            int: Records count.
        """

        return self.history.count(filters)

    count_history = deprecated(
        _count_history, reason='Use `Module.history.count` insted.')

    def _undo_history(self, history):
        """Undo a history.

        Args:
            history (HistoryInfo): History information.
        """

        self.history.undo(history)

    undo_history = deprecated(
        _undo_history, reason='Use `Module.history.undo` insted.')
