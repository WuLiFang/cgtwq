# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none
"""CGTeamWork python client for humans.  """

from __future__ import absolute_import, print_function, unicode_literals

from ._client_impl import new_client
from ._row_id import RowID
from ._field_sign import FieldSign as F, FieldSign
from ._user_token import UserToken
from ._message import Message as MessageV2

TYPE_CHECKING = False
if TYPE_CHECKING:
    from ._client import Client
    from ._flow_service import FlowService
    from ._plugin_service import PluginService
    from ._pipeline_service import PipelineService

    __all__ = [
        "new_client",
        "RowID",
        "FieldSign",
        "F",
        "Client",
        "FlowService",
        "PluginService",
        "PipelineService",
        "UserToken",
        "MessageV2",
        # legacy export,
        "server",
        "get_account",
        "get_account_id",
        "login",
        "DesktopClient",
        "Database",
        "AccountError",
        "AccountNotFoundError",
        "CGTeamWorkException",
        "EmptySelection",
        "IDError",
        "LoginError",
        "PasswordError",
        "PermissionError",
        "PrefixError",
        "SignError",
        "Field",
        "Filter",
        "FilterList",
        "Message",
        "Module",
        "PluginMeta",
        "ACCOUNT",
        "PROJECT",
        "ResultSet",
        "Entry",
        "Selection",
        "current_account",
        "current_account_id",
        "update_setting",
        "compat",
        "__version__",
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
from deprecated import deprecated  # type: ignore
from . import __version__, compat

get_all_status = deprecated(  # type: ignore
    version="3.0.0", reason="Use server.meta.get_status instead"
)(server.meta.get_status)
