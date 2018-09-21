# -*- coding=UTF-8 -*-
"""Create http connection with cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import logging
from collections import OrderedDict

import requests

from .. import core, exceptions

LOGGER = logging.getLogger(__file__)
SESSION = requests.Session()


def _json_default(self, obj):
    if isinstance(obj, OrderedDict):
        return dict(obj)
    return json.JSONEncoder.default(self, obj)


def _raise_error(result):
    if not isinstance(result, dict):
        return

    code, type_, data = (result.get('code'),
                         result.get('type'),
                         result.get('data', result))

    if code is None:
        return
    elif code == '1':
        return
    elif (code, type_, data) == ('2', 'msg', 'please login!!!'):
        raise exceptions.LoginError
    raise ValueError(data)


def call(controller, method, token, ip=None, **data):
    """Call method on server controller.

    Args:
        controller (str): Controller name.
        method (str): Method name.
        token (str): User token.
        ip (str, optional): Defaults to None. Server IP.

    Returns:
        Method result.
    """

    data['controller'] = controller
    data['method'] = method

    return post('api.php', data, token, ip)


def post(pathname, data, token, ip=None, **kwargs):
    """`POST` data to CGTeamWork server.
        pathname (str unicode): Pathname for http host.
        ip (str unicode, optional): Defaults to None. If `ip` is None,
            will use ip from setting or setting.
        data: Data to post.
        **kwargs: kwargs for `requests.post`

    Returns:
        Server execution result.
    """
    # pylint: disable=invalid-name

    assert 'cookies' not in kwargs
    assert 'data' not in kwargs

    ip = ip or core.CONFIG['SERVER_IP']
    cookies = {'token': token}
    LOGGER.debug('POST: %s: %s', pathname, data)
    if data is not None:
        data = {'data': json.JSONEncoder(default=_json_default).encode(data)}
    resp = SESSION.post('http://{}/{}'.format(ip, pathname.lstrip('\\/')),
                        data=data,
                        cookies=cookies,
                        **kwargs)
    LOGGER.debug('RECV: %s', resp.text.strip())
    json_ = resp.json()
    _raise_error(json_)
    if not isinstance(json_, dict):
        return json_
    return json_.get('data', json_)


def get(pathname, token, ip=None, **kwargs):
    """`GET` request to CGTeamWork server.
        token (str unicode, optional): Defaults to None. If `token` is None,
            will use token from setting.
        ip (str unicode, optional): Defaults to None. If `ip` is None,
            will use ip from setting.
        **kwargs: kwargs for `requests.get`

    Returns:
        json server response .
    """
    # pylint: disable=invalid-name

    assert 'cookies' not in kwargs
    ip = ip or core.CONFIG['SERVER_IP']
    cookies = {'token': token}

    LOGGER.debug('GET: kwargs: %s', kwargs)
    resp = SESSION.get('http://{}/{}'.format(ip, pathname.lstrip('\\/')),
                       cookies=cookies,
                       **kwargs)
    LOGGER.debug('GET: %s', resp.text.strip())
    json_ = resp.json()
    _raise_error(json_)
    if not isinstance(json_, dict):
        return json_
    return json_.get('data', json_)
