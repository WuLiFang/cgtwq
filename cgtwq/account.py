# -*- coding=UTF-8 -*-
"""Cgteamwork account operations.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import core, server
from .exceptions import AccountNotFoundError, PasswordError
from .model import AccountInfo


def get_account(token=None):
    """Get account from token.

    Args:
        token (str): Server token

    Returns:
        str: Account name.
    """

    token = core.CONFIG['DEFAULT_TOKEN']
    return server.call("c_token", "get_account", token=token)


def get_account_id(token=None):
    """Get account id from token.

    Args:
        token (str): Server token

    Returns:
        str: Account id.
    """

    token = core.CONFIG['DEFAULT_TOKEN']
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
    assert isinstance(resp, dict), type(resp)
    # Correct server-side typo.
    resp['password_complexity'] = (
        # spell-checker: disable
        resp.pop('password_comlexity', None)
        # spell-checker: enable
    )
    _ = [resp.setdefault(i, None) for i in AccountInfo._fields]
    return AccountInfo(**resp)


def get_online_account_id(token=None):
    token = token or core.CONFIG['DEFAULT_TOKEN']
    resp = server.call(
        'c_token', 'get_all_online_account_id_with_type', token=token)
    return resp
