# -*- coding=UTF-8 -*-
"""Cgteamwork account operations.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from collections import namedtuple

from . import server

AccountInfo = namedtuple('AccountInfo',
                         ('account', 'account_id', 'image',
                          'update_time', 'file_key', 'token',
                          'client_type', 'remote_ip', 'name'))


def get_account(token):
    """Get current account.

    Returns:
        str: Account name.
    """
    return server.call("c_token", "get_account", token=token).data


def get_account_id(token):
    """Get current acccount id.

    Returns:
        unicode: account id.
    """
    return server.call("c_token", "get_account_id", token=token).data


def login(account, password):
    """Login on server.

    Args:
        account (str): Account name.
        password (str): Password.

    Raises:
        ValueError: When login fail.

    Returns:
        AccountInfo: Account information.
    """

    resp = server.call("c_token", "login",
                       account=account,
                       password=password,
                       token='',
                       client_type="py")
    return AccountInfo(**resp.data)
