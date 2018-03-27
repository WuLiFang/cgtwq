# -*- coding=UTF-8 -*-
"""Database in cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

from .client import DesktopClient

from .server import setting
from . import account
LOGGER = logging.getLogger(__name__)


def update_setting():
    """Update setting from client.   """

    setting.SERVER_IP = DesktopClient.server_ip()
    setting.DEFAULT_TOKEN = DesktopClient.token()


def current_account_id():
    """Get account id from desktop client.  """

    return account.get_account_id(DesktopClient.token())


def current_account():
    """Get account from desktop client.  """

    return account.get_account(DesktopClient.token())
