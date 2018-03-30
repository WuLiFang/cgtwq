# -*- coding=UTF-8 -*-
"""Database module.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

from six import text_type

from .filter import Filter, FilterList
from .model import HistoryInfo
from .selection import Selection

LOGGER = logging.getLogger(__name__)


class Module(object):
    """Module(Database table) in database.    """
    _token = None

    def __init__(self, name, database):
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

    def __getitem__(self, name):
        if isinstance(name, (Filter, FilterList)):
            return self.filter(name)
        return self.select(name)

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
        return self.database.call(*args, module=self.name, **kwargs)

    def select(self, *id_list):
        """Create selection on this module.

        Args:
            *id_list (text_type): Id list to select.

        Returns:
            Selection: Created selection.
        """

        return Selection(self, *id_list)

    def filter(self, filters):
        """Create selection with filter on this module.

        Args:
            filters (FilterList, Filter): Filters for server.

        Returns:
            Selection: Created selection.
        """

        _filters = self.format_filters(filters)
        resp = self.call('c_orm', 'get_with_filter',
                         sign_array=[self.field('id')],
                         sign_filter_array=_filters)
        if resp.data:
            id_list = [i[0] for i in resp.data]
        else:
            id_list = []
        return Selection(self, *id_list)

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
        return '{}.{}'.format(self.name, name)

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

        resp = self.call(
            "c_history", "get_with_filter",
            field_array=HistoryInfo.fields,
            filter_array=FilterList(filters))
        return tuple(HistoryInfo(*i) for i in resp.data)

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
        return int(resp.data)
