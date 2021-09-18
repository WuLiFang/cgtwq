# -*- coding=UTF-8 -*-
"""Database on cgtw server.  """
from __future__ import absolute_import, division, print_function, unicode_literals


TYPE_CHECKING = False
if TYPE_CHECKING:
    import cgtwq


class DatabaseAttachment(object):
    """Attachment feature for database."""

    # pylint: disable=too-few-public-methods

    def __init__(self, database):
        # type: (cgtwq.Database) -> None
        from .database import Database

        assert isinstance(database, Database)
        self.database = database
        self.call = self.database.call
