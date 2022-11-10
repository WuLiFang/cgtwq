# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Any

from six import python_2_unicode_compatible  # type: ignore


@python_2_unicode_compatible
class RowID:
    def __init__(self, database, module, module_type, value):
        # type: (Text, Text, Text, Text) -> None
        self._database = database
        self._module = module
        self._module_type = module_type
        self._value = value

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, RowID):
            return False
        return self.__str__() == other.__str__()

    def __ne__(self, other):
        # type: (Any) -> bool
        return not self.__eq__(other)

    @property
    def database(self):
        return self._database

    @property
    def module(self):
        return self._module

    @property
    def module_type(self):
        return self._module_type

    @property
    def value(self):
        return self._value

    def __str__(self):
        return "row-id:///%s/%s/%s/%s" % (
            self._database,
            self._module,
            self._module_type,
            self._value,
        )

    __repr__ = __str__
