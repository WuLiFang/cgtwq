# -*- coding=UTF-8 -*-
"""Create http connection with cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import logging

import requests

from ..client import CGTeamWorkClient

LOGGER = logging.getLogger(__file__)

from .. import setting


def post(pathname, data, ip=None, **kwargs):
    """Post data to CGTeamWork server.
        pathname (str unicode): Pathname for http host.
        ip (str unicode, optional): Defaults to None. If `ip` is None,
            will use ip from setting or CGTeamWorkClient.
        data: Data to post.
        **kwargs: kwargs for `requests.post`

    Returns:
        Server execution result.
    """

    assert 'cookies' not in kwargs
    assert 'data' not in kwargs
    token = data.get('token', CGTeamWorkClient.token())
    data['token'] = token
    ip = ip or setting.SERVER_IP or CGTeamWorkClient.server_ip()
    cookies = {'token': token}

    resp = requests.post('http://{}/{}'.format(ip, pathname.lstrip('\\/')),
                         data={'data': json.dumps(data)},
                         cookies=cookies,
                         **kwargs)
    json_ = resp.json()
    result = json_.get('data', json_)
    if (isinstance(json_, dict)
            and (json_.get('code'), json_.get('type')) == ('0', 'msg')):
        raise ValueError(result)

    return result


def get(pathname, token=None, ip=None, **kwargs):
    """Get request to CGTeamWork server.
        token (str unicode, optional): Defaults to None. If `token` is None,
            will use token from CGTeamWorkClient.
        ip (str unicode, optional): Defaults to None. If `ip` is None,
            will use ip from CGTeamWorkClient.
        **kwargs: kwargs for `requests.get`

    Returns:
        [type]: [description]
    """

    assert 'cookies' not in kwargs
    token = token or CGTeamWorkClient.token()
    ip = ip or CGTeamWorkClient.server_ip()
    cookies = {'token': token}

    LOGGER.debug('GET: kwargs: %s', kwargs)
    resp = requests.get('http://{}/{}'.format(ip, pathname.lstrip('\\/')),
                        cookies=cookies,
                        **kwargs)
    try:
        result = json.loads(resp.content)
    except ValueError:
        result = None
    if (isinstance(result, dict)
            and (result.get('code'), result.get('type')) == ('0', 'msg')):
        raise ValueError(result.get('data', result))
    LOGGER.debug('GET: %s', result)
    return resp
