# -*- coding=UTF-8 -*-
"""CGTeamWork python client for humans.  """


from __future__ import absolute_import, print_function, unicode_literals

from wlf.decorators import renamed

from . import server
from .account import get_account, get_account_id, login
from .client import DesktopClient
from .database import Database
from .exceptions import (AccountError, AccountNotFoundError,
                         CGTeamWorkException, EmptySelection, IDError,
                         LoginError, PasswordError, PermissionError,
                         PrefixError, SignError)
from .filter import Field, Filter, FilterList
from .message import Message
from .module import Module
from .plugin_meta import PluginMeta
from .public_module import ACCOUNT, PROJECT
from .resultset import ResultSet
from .selection import Entry, Selection
from .util import current_account, current_account_id, update_setting

# Depreacted names.
# TODO: Remove at next major version.
renamed('get_all_status')(server.meta.get_status)

__all__ = ['login', 'get_account',
           'get_account_id', 'DesktopClient', 'Database',
           'server', 'Field', 'Filter', 'FilterList',
           'Message', 'Module', 'PluginMeta',
           'ACCOUNT', 'PROJECT', 'ResultSet', 'Entry',
           'Selection', 'AccountError', 'AccountNotFoundError',
           'CGTeamWorkException', 'IDError', 'LoginError', 'PasswordError',
           'PermissionError', 'PrefixError', 'SignError','EmptySelection']
