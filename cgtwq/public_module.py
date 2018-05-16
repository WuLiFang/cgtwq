# -*- coding=UTF-8 -*-
"""Database module.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .database import Database
from .filter import Filter
from .module import Module


class PublicModule(Module):
    """Module in special `public` database.    """

    def __init__(self, name, active_filter, name_field):
        self.database = Database('public')
        self.active_filter = active_filter
        self.name_field = name_field
        super(PublicModule, self).__init__(name, self.database)

    def all(self):
        """All active entries.

        Returns:
            Selection
        """

        return self.filter(self.active_filter)

    def names(self):
        """All actived entries label.

        Returns:
            tuple[str]
        """

        return self.all()[self.name_field]


PROJECT = PublicModule('project', Filter('status', 'Active'), 'full_name')
ACCOUNT = PublicModule('account', Filter('status', 'Y'), 'name')
