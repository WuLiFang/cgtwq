# -*- coding=UTF-8 -*-
"""Database on cgtw server.  """
from __future__ import absolute_import, division, print_function, unicode_literals

from . import core

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Text
    import cgtwq


class DatabaseMeta(core.DatabaseAttachment):
    """Database metadate accessor."""

    # pylint: disable=too-few-public-methods

    def __init__(self, database, is_user):
        # type: (cgtwq.Database, bool) -> None
        super(DatabaseMeta, self).__init__(database)
        self.is_user = is_user

    def __getitem__(self, key):
        # type: (Text) -> Any
        return self.call(
            "c_api_data", "get_user" if self.is_user else "get_common", key=key
        )

    def __setitem__(self, key, value):
        # type: (Text, Any) -> None
        self.call(
            "c_api_data",
            "set_user" if self.is_user else "set_common",
            key=key,
            value=value,
        )
