# -*- coding=UTF-8 -*-
"""Filter used on cgtw server.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six
from six.moves import reduce

# six.moves.collections_abc is not added at six<1.13.0
# https://github.com/benjaminp/six/blob/42636b15dd1a5b85de56eac98e47954d4c776576/CHANGES#L35
if six.PY3:
    from collections.abc import Iterable
else:
    from collections import Iterable

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, List, Text, Union


class Filter(list):
    """CGTeamWork style filter.  """

    def __init__(self, key, value, operator=None):
        # type: (Text, Any, Text) -> None
        if operator is None:
            operator = 'in' if isinstance(value, (list, tuple)) else '='
        super(Filter, self).__init__((key, operator, value))

    def __and__(self, other):
        # type: (Union[Filter, FilterList]) -> FilterList
        return FilterList(self) & FilterList(other)

    def __or__(self, other):
        # type: (Union[Filter, FilterList]) -> FilterList
        return FilterList(self) | FilterList(other)

    def in_namespace(self, namespace):
        # type: (Text) -> Filter
        """Get a new `Filter` instance in the namespace.

        Args:
            namespace (str): Default namespace for keys.

        Returns:
            Filter
        """

        key, operator, value = self
        return self.from_list(
            [Field(key).in_namespace(namespace), operator, value])

    @classmethod
    def from_list(cls, obj):
        # type: (List[Any]) -> Filter
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
    """CGTeamWork style filter list.  """

    def __init__(self, list_):
        # type: (Union[Filter, Iterable[Any]]) -> None
        if isinstance(list_, Filter):
            list_ = [list_]
        elif isinstance(list_, Iterable):
            list_ = list(list_)
            if not all(isinstance(i, (Filter, str, six.text_type)) for i in list_):
                raise ValueError('Malformed list', list_)
        super(FilterList, self).__init__(list_)

    def _combine(self, other, operator):
        # type: (Union[FilterList, Filter], Text) -> FilterList
        ret = FilterList(self)
        ret.append(operator)
        ret += FilterList(other)
        return ret

    def __and__(self, other):
        # type: (Union[FilterList, Filter]) -> FilterList
        return self._combine(other, 'and')

    def __or__(self, other):
        # type: (Union[FilterList, Filter]) -> FilterList
        return self._combine(other, 'or')

    def in_namespace(self, namespace):
        # type: (Text) -> FilterList
        """Create new `FilterList` instance in the namespace.

        Args:
            namespace (str): Default namespace for keys.

        Returns:
            FilterList
        """

        return FilterList(i.in_namespace(namespace)
                          if isinstance(i, Filter) else i
                          for i in self)

    @classmethod
    def from_arbitrary_args(cls, *filters):
        # type: (Union[Filter, FilterList]) -> FilterList
        """Create filterlist from arbitrary arguments.

        Returns:
            FilterList
        """

        ret = [i if isinstance(i, (Filter, FilterList)) else Filter.from_list(i)
               for i in filters]
        if ret:
            ret = reduce(lambda a, b: a & b, ret)  # type: ignore
        return cls(ret)


class Field(six.text_type):
    """Data base field name for filter.  """

    def __hash__(self):
        return six.text_type(self).__hash__()

    def __or__(self, value):
        # type: (Any) -> Filter
        return self.in_(value)

    def __and__(self, value):
        # type: (Any) -> Filter
        return self.has(value)

    def __eq__(self, value):
        # type: (Any) -> Filter
        return Filter(self, value, '=')

    def __gt__(self, value):
        # type: (Any) -> Filter
        return Filter(self, value, '>')

    def __lt__(self, value):
        # type: (Any) -> Filter
        return Filter(self, value, '<')

    def in_(self, value):
        # type: (Any) -> Filter
        """Represents matched data in value list.  """
        if isinstance(value, (str, six.text_type)):
            value = [value]
        return Filter(self, value, 'in')

    def has(self, value):
        # type: (Any) -> Filter
        """Represents data has value in it.  """
        return Filter(self, value, 'has')

    def contains(self, value):
        # type: (Any) -> Filter
        """Represents value in data item list.  """
        return Filter(self, value, 'concat')

    def in_namespace(self, namespace):
        # type: (Text) -> Field
        """Get a new `Field` instance in the namespace.

        Args:
            namespace (str): Default namespace for keys.

        Returns:
            Field
        """

        key = self
        if not ('.' in key or '#' in key):
            key = '{}.{}'.format(namespace, key)
        return Field(key)
