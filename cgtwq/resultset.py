# -*- coding=UTF-8 -*-
"""Database query result set.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

import six

from .filter import Field

LOGGER = logging.getLogger(__name__)


class ResultSet(list):
    """Database query result.  """

    def __init__(self, roles, data, module):
        from .module import Module
        assert isinstance(module, Module)
        assert all(isinstance(i, list) and len(i) == len(roles)
                   for i in data), data
        super(ResultSet, self).__init__(data)
        self.module = module
        self.roles = [six.text_type(i) for i in roles]

    def column(self, field):
        """Get a column from field name.

        Args:
            field (text_type): Field name.

        Returns:
            tuple: Column data.
        """

        field = Field(field).in_namespace(self.module.default_field_namespace)
        index = self.roles.index(six.text_type(field))
        return tuple(sorted(set(i[index] for i in self)))
