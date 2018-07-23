# -*- coding=UTF-8 -*-
"""CGTeamWork python client for humans.  """


from __future__ import absolute_import, print_function, unicode_literals

from .account import get_account, get_account_id, login
from .client import DesktopClient
from .database import Database
from .exceptions import (AccountError, AccountNotFoundError,
                         CGTeamWorkException, IDError, LoginError,
                         PasswordError, PermissionError, PrefixError,
                         SignError)
from .filter import Field, Filter, FilterList
from .module import Module
from .public_module import ACCOUNT, PROJECT
from .resultset import ResultSet
from .selection import Entry, Selection
from .status import get_all as get_all_status
from .util import current_account, current_account_id, update_setting
