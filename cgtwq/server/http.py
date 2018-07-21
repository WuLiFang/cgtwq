# -*- coding=UTF-8 -*-
"""Create http connection with cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import logging

import requests

from . import setting
from .. import exceptions

LOGGER = logging.getLogger(__file__)
SESSION = requests.Session()

def _raise_error(result):
    if not isinstance(result, dict):
        return
    code, type_, data = (result.get('code'), result.get(
        'type'), result.get('data', result))
    if code == '1':
        return

    if (code, type_, data) == ('2', 'msg', 'please login!!!'):
        raise exceptions.LoginError
    raise ValueError(data)


def call(controller, method, token, ip=None, **data):
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

    ip = ip or setting.SERVER_IP
    cookies = {'token': token}
    LOGGER.debug('POST: %s: %s', pathname, data)
    if data is not None:
        data = {'data': json.dumps(data)}
    resp = SESSION.post('http://{}/{}'.format(ip, pathname.lstrip('\\/')),
                         data=data,
                         cookies=cookies,
                         **kwargs)
    LOGGER.debug('RECV: %s', resp.text)
    json_ = resp.json()
    _raise_error(json_)
    return json_.get('data', json_)


def get(pathname, token, ip=None, **kwargs):
    """`GET` request to CGTeamWork server.
        token (str unicode, optional): Defaults to None. If `token` is None,
            will use token from setting.
        ip (str unicode, optional): Defaults to None. If `ip` is None,
            will use ip from setting.
        **kwargs: kwargs for `requests.get`

    Returns:
        [type]: [description]
    """
    # pylint: disable=invalid-name

    assert 'cookies' not in kwargs
    ip = ip or setting.SERVER_IP
    cookies = {'token': token}

    LOGGER.debug('GET: kwargs: %s', kwargs)
    resp = SESSION.get('http://{}/{}'.format(ip, pathname.lstrip('\\/')),
                        cookies=cookies,
                        **kwargs)
    try:
        result = json.loads(resp.content)
    except ValueError:
        result = None
    _raise_error(result)
    LOGGER.debug('GET: %s', result)
    return resp
