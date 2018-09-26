# -*- coding=UTF-8 -*-
"""Database query result set.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

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
        self.roles = roles

    def column(self, field):
        """Get a column from field name.

        Args:
            field (text_type): Field name.

        Returns:
            tuple: Column data.
        """

        field = self.module.format_field(field)
        index = self.roles.index(field)
        return tuple(sorted(set(i[index] for i in self)))
