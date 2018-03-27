# -*- coding=UTF-8 -*-
"""Create websocket connection with cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import logging
from collections import namedtuple
from contextlib import contextmanager

import websocket

from ..client import CGTeamWorkClient
from ..exceptions import LoginError
from .. import setting

LOGGER = logging.getLogger(__name__)

Response = namedtuple('Response', ['data', 'code', 'type'])


@contextmanager
def connection(ip=None, port=8888):
    """Create connection to server.

    Decorators:
        contextmanager

    Args:
        ip (unicode, optional): Defaults to None. Server ip,
            if `ip` is None, will try use ip from running client.
        port (int, optional): Defaults to 8888. Server port.

    Returns:
        websocket.WebSocket: Connected soket.
    """
    # pylint: disable=invalid-name

    ip = ip or setting.SERVER_IP
    url = 'ws://{}:{}'.format(ip, port)
    conn = websocket.create_connection(url)
    assert isinstance(conn, websocket.WebSocket)
    try:
        yield conn
    finally:
        conn.close()


def parse_recv(payload):
    """Parse server response

    Args:
        payload (bytes): Server defined response.

    Returns:
        Response: Parsed payload.
    """

    resp = json.loads(payload)
    data = resp['data']
    code = int(resp['code'])
    type_ = resp['type']
    return Response(data, code, type_)


def call(controller, method, token=None, **kwargs):
    """Send command to server, then get response.

    Args:
        controller (str): Server defined controller.
        method (str): Server defined controller method.
        token (str): Defalts to None, User token.
            If token is None, will try get token from cgtw desktop client.
        ip (str): Server websocket ip.
        **kwargs : Server defined keyword arguments for method.

    Raises:
        LoginError: When not loged in .
        ValueError: When server call failed.

    Returns:
        Response: Server response.
    """
    # pylint: disable=invalid-name
    if token is None:
        token = CGTeamWorkClient.token()
    payload = {'controller': controller,
               'method': method,
               'token': token}
    payload.update(kwargs)
    with connection() as conn:
        assert isinstance(conn, websocket.WebSocket)
        conn.send(json.dumps(payload))
        LOGGER.debug('SEND: %s', repr(payload))
        recv = conn.recv()
        LOGGER.debug('RECV: %s', recv)
        resp = parse_recv(recv)
        if resp.data == 'please login!!!':
            raise LoginError(resp)
        if (resp.code, resp.type) == (0, 'msg'):
            raise ValueError(resp.data)
        return resp
