# -*- coding=UTF-8 -*-
# pyright: basic, reportTypeCommentUsage=none,reportUnusedImport=none
"""CGTeamWork python client for humans.  """

from __future__ import absolute_import, print_function, unicode_literals

from ._client import ClientImpl as Client
from ._row_id import RowID
from ._field_sign import FieldSign as F, FieldSign

__all__ = [
    "Client",
    "RowID",
    "FieldSign",
    "F",
]

from . import server
from .account import get_account, get_account_id, login
from .client import DesktopClient
from .database import Database
from .exceptions import (
    AccountError,
    AccountNotFoundError,
    CGTeamWorkException,
    EmptySelection,
    IDError,
    LoginError,
    PasswordError,
    PermissionError,
    PrefixError,
    SignError,
)
from .filter import Field, Filter, FilterList
from .message import Message
from .module import Module
from .plugin_meta import PluginMeta
from .public_module import ACCOUNT, PROJECT
from .resultset import ResultSet
from .selection import Entry, Selection
from .util import current_account, current_account_id, update_setting
from deprecated import deprecated
from . import __version__, compat

get_all_status = deprecated(
    version="3.0.0", reason="Use server.meta.get_status instead"
)(server.meta.get_status)
