# -*- coding=UTF-8 -*-
"""Database in cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

from wlf.decorators import deprecated

from . import account, core
from .client import DesktopClient

LOGGER = logging.getLogger(__name__)


@deprecated('update_setting', reason='Use `DesktopClient.connect` instead.')
def _update_setting():
    """Update setting from client.   """

    DesktopClient().connect()


@deprecated('current_account_id', reason='Use `account.get_account_id` instead.')
def _current_account_id():
    """Get account id from desktop client.  """

    return account.get_account_id()


@deprecated('current_account', reason='Use `account.get_account` instead.')
def _current_account():
    """Get account from desktop client.  """

    return account.get_account()
