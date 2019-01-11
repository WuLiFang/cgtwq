# -*- coding=UTF-8 -*-
"""Database module.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from wlf.decorators import deprecated

from .database import Database
from .filter import Field, Filter
from .module import Module


class PublicModule(Module):
    """Module in special `public` database.    """

    def __init__(self, name, active_filter, name_field, module_type='info'):
        self.database = Database('public')
        self.active_filter = active_filter
        self.name_field = name_field
        self.default_field_namespace = name
        super(PublicModule, self).__init__(name, self.database, module_type)

    def select_all(self):
        """Select all entries.

        Returns:
            Selection
        """

        return self.filter(Field(self.name_field).has('%'))

    def select_activated(self):
        """Select all active entries.

        Returns:
            Selection
        """
        return self.filter(self.active_filter)

    def names(self):
        """All actived entries label.

        Returns:
            tuple[str]
        """

        return self.select_activated()[self.name_field]

    # Deprecated methods
    all = deprecated(
        select_activated,
        reason='Use `PublicModule.select_activated` insted.')


PROJECT = PublicModule('project', Filter('status', 'Active'), 'full_name')
ACCOUNT = PublicModule('account', Filter('status', 'Y'), 'name')
