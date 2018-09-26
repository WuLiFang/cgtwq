# -*- coding=UTF-8 -*-
"""Database module.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

import six
from six import text_type
from six.moves import reduce

from .core import ControllerGetterMixin
from .filter import Filter, FilterList
from .model import FieldInfo, FlowInfo, HistoryInfo
from .selection import Selection

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
        from .database import Database
        assert isinstance(database, Database)
        self.database = database
        self.module_type = module_type
        self.label = None
        self._token = None

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
                         sign_array=(self.field('id'),),
                         sign_filter_array=_filters)
        if resp:
            id_list = [i[0] for i in resp]
        else:
            id_list = []
        return Selection(self, *id_list)

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

    def field(self, name):
        """Formatted field name for this module.

        Args:
            name (text_type): Short field name.

        Returns:
            text_type: Full field name, for server.
        """

        assert isinstance(name, (str, text_type))
        if ('.' in name
                or '#' in name):
            return name
        return '{}.{}'.format(self.default_field_namespace, name)

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
                i[0] = self.field(i[0])
        return ret

    def pipelines(self):
        """All pipeline in this module.

        Returns:
            tuple[Pipeline]: namedtuple for ('id', 'name', 'module').
        """

        return self.database.get_pipelines(Filter('module', self.name))

    def get_history(self, filters):
        """Get history record from the module.
            filters (Filter or FilterList): History filters.

        Returns:
            tuple[HistoryInfo]: History records.
        """

        return self._get_model(
            "c_history", "get_with_filter",
            HistoryInfo, filters
        )

    def count_history(self, filters):
        """Count history records in the module.

        Args:
            filters (Filter or FilterList):
                History filters.

        Returns:
            int: Records count.
        """

        resp = self.call(
            "c_history", "count_with_filter",
            filter_array=FilterList(filters))
        return int(resp)

    def undo_history(self, history):
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

    def flow(self):
        """Workflow of the module.  """

        resp = self.call('c_flow', 'get_data')
        return tuple(FlowInfo(*i) for i in resp)

    def fields(self):
        """Get fields in this module.  """

        resp = self.call(
            'c_field', 'get_join_module_data',
            field_array=FieldInfo.fields,
            order_field_array=["module", "sort_id"],
        )
        return tuple(FieldInfo(*i) for i in resp)

    def create_field(self, sign, type_, name=None, label=None):
        """Create new field in the module.

        Args:
            sign (str): Field sign
            type_ (str): Field type, see `core.FIELD_TYPES`.
            name (str, optional): Defaults to None. Field english name.
            label (str, optional): Defaults to None. Field chinese name.
        """

        if '.' not in sign:
            module = self.name if self.module_type != 'task' else 'task'
            sign = '{}.{}'.format(module, sign)
        self.database.create_field(
            sign=sign, type_=type_, name=name, label=label)

    def delete_field(self, id_):
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
