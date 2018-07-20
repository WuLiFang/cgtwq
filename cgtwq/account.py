# -*- coding=UTF-8 -*-
"""Cgteamwork account operations.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import server
from .exceptions import AccountNotFoundError, PasswordError
from .model import AccountInfo


def get_account(token):
    """Get account from token.

    Args:
        token (str): Server token

    Returns:
        str: Account name.
    """

    return server.call("c_token", "get_account", token=token)


def get_account_id(token):
    """Get account id from token.

    Args:
        token (str): Server token

    Returns:
        str: Account id.
    """
    return server.call("c_token", "get_account_id", token=token)


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

    try:
        resp = server.call("c_token", "login",
                           account=account,
                           password=password,
                           token="",
                           client_type="py")
    except ValueError as ex:
        try:
            raise {
                'token::login, get account data error': AccountNotFoundError(account),
                'token::login, 密码错误,请检查': PasswordError,
            }[ex.args[0]]
        except (KeyError, IndexError):
            pass
        raise

    return AccountInfo(**resp)


def get_online_account_id(token=None):
    token = token or server.setting.DEFAULT_TOKEN
    resp = server.call(
        'c_token', 'get_all_online_account_id_with_type', token=token)
    return resp
