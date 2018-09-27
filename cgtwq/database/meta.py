
# -*- coding=UTF-8 -*-
"""Database on cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import core


class DatabaseMeta(core.DatabaseAttachment):
    """Database metadate accessor.  """
    # pylint: disable=too-few-public-methods

    def __init__(self, database, is_user):
        super(DatabaseMeta, self).__init__(database)
        self.is_user = is_user

    def __getitem__(self, key):
        return self.call(
            "c_api_data",
            'get_user' if self.is_user else 'get_common',
            key=key)

    def __setitem__(self, key, value):
        self.call(
            "c_api_data",
            'set_user' if self.is_user else 'set_common',
            key=key, value=value)
