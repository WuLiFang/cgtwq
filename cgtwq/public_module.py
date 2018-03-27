# -*- coding=UTF-8 -*-
"""Database module.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

from six import text_type

from .module import Module
from .database import Database
from .filter import Filter, FilterList
from .model import (FIELDS_FILEBOX, FIELDS_HISTORY, FIELDS_NOTE,
                    FIELDS_PIPELINE, FileBoxDetail, FileBoxInfo, HistoryInfo,
                    ImageInfo, NoteInfo, PipelineInfo)
from .selection import Selection

LOGGER = logging.getLogger(__name__)


class PublicModule(Module):
    """Module in special `public` database.    """

    def __init__(self):
        self.database = Database('public')
        super(PublicModule, self).__init__(self.name, self.database)


class Project(PublicModule):
    """Module to keep project information.   """

    name = 'project'

    def all(self):
        """All active project.

        Returns:
            Selection: Projects.
        """

        return self.filter(Filter('status', 'Active'))

    def names(self):
        """All actived project names.

        Returns:
            tuple
        """

        return self.all()['full_name']


PROJECT = Project()


class Account(PublicModule):
    """Module to keep account information.   """

    name = 'account'

    def all(self):
        """All active user  .

        Returns:
            Selection: Users.
        """

        return self.filter(Filter('status', 'Y'))

    def names(self):
        """All user names.

        Returns:
            tuple
        """

        return self.all()['name']


ACCOUNT = Account()
