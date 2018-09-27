# -*- coding=UTF-8 -*-
"""Filter used on cgtw server.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from collections import Iterable

from six import text_type


class Filter(list):
    """CGteamwork style filter.  """

    def __init__(self, key, value, operator=None):
        if operator is None:
            operator = 'in' if isinstance(value, (list, tuple)) else '='
        super(Filter, self).__init__((key, operator, value))

    def __and__(self, other):
        return FilterList(self) & FilterList(other)

    def __or__(self, other):
        return FilterList(self) | FilterList(other)

    def in_namespace(self, namespace):
        """Get a new `Filter` instance in the namespace.

        Args:
            namespace (str): Default namespace for keys.

        Returns:
            Filter
        """

        key, operator, value = self
        if not ('.' in key or '#' in key):
            key = '{}.{}'.format(namespace, key)
        return self.from_list([key, operator, value])

    @classmethod
    def from_list(cls, obj):
        """Create filter instance from a list.

        Args:
            obj (list): A list match [key, operater, value].

        Raises:
            ValueError: can not convert `obj` to filter.

        Returns:
            Filter
        """

        if not len(obj) == 3:
            raise ValueError('Can not convert to filter.', obj)
        return cls(obj[0], obj[2], obj[1])


class FilterList(list):
    """CGteamwork style filter list.  """

    def __init__(self, list_):
        if isinstance(list_, Filter):
            list_ = [list_]
        elif isinstance(list_, Iterable):
            list_ = list(list_)
            assert all(isinstance(i, Filter) for i in list_), \
                'Some item in the list is not a filter'
        super(FilterList, self).__init__(list_)

    def _combine(self, other, operator):
        ret = FilterList(self)
        ret.append(operator)
        ret += FilterList(other)
        return ret

    def __and__(self, other):
        return self._combine(other, 'and')

    def __or__(self, other):
        return self._combine(other, 'or')

    def in_namespace(self, namespace):
        """Create new `FilterList` instance in the namespace.

        Args:
            namespace (str): Default namespace for keys.

        Returns:
            FitlerList
        """

        return FilterList(i.in_namespace(namespace) for i in self)

    @classmethod
    def from_arbitrary_args(cls, *filters):
        """Create filterlist from arbitrary arguments.

        Returns:
            FilterList
        """

        ret = [i if isinstance(i, (Filter, FilterList)) else Filter.from_list(i)
               for i in filters]
        ret = reduce(lambda a, b: a & b, ret)
        return cls(ret)


class Field(text_type):
    """Data base field name for filter.  """

    def __or__(self, value):
        return self.in_(value)

    def __and__(self, value):
        return self.has(value)

    def __eq__(self, value):
        return Filter(self, value, '=')

    def __gt__(self, value):
        return Filter(self, value, '>')

    def __lt__(self, value):
        return Filter(self, value, '<')

    def in_(self, value):
        """Represents matched data in value list.  """
        if isinstance(value, (str, text_type)):
            value = [value]
        return Filter(self, value, 'in')

    def has(self, value):
        """Represents data has value in it.  """
        return Filter(self, value, 'has')

    def contains(self, value):
        """Represents value in data item list.  """
        return Filter(self, value, 'concat')
