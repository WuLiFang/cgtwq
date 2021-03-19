# -*- coding=UTF-8 -*-
"""Database in cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

from deprecated import deprecated

from . import account
from .client import DesktopClient

LOGGER = logging.getLogger(__name__)


@deprecated(
    version='3.0.0',
    reason='Use `DesktopClient.connect` instead.',
)
def update_setting():
    """Update setting from client.   """

    DesktopClient().connect()


@deprecated(
    version='3.0.0',
    reason='Use `account.get_account_id` instead.',
)
def current_account_id():
    """Get account id from desktop client.  """

    return account.get_account_id()


@deprecated(
    version='3.0.0',
    reason='Use `account.get_account` instead.',
)
def current_account():
    """Get account from desktop client.  """

    return account.get_account()
