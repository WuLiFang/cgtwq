# -*- coding=UTF-8 -*-
"""Desktop client.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import logging
import socket

import six
from websocket import create_connection

from ...core import CONFIG

LOGGER = logging.getLogger(__name__)


class DesktopClientAttachment(object):
    """Attachment feature for desktop client.  """
    # pylint: disable=too-few-public-methods

    def __init__(self, client):
        from .client import DesktopClient
        assert isinstance(client, DesktopClient)
        self.client = client


def call(socket_url, controller, method, **kwargs):
    """Call method on the cgteamwork client.

    Args:
        socket_url(str): Desktop client websocket url.
        controller(str): Client defined controller name.
        method (str): Client defined method name
            on the controller.
        **kwargs: Client defined method keyword arguments.

    Returns:
        dict or str: Received data.
    """

    payload = dict(sign=controller, method=method, **kwargs)
    payload.setdefault('type', 'get')

    conn = create_connection(socket_url, CONFIG['CONNECTION_TIMEOUT'])

    try:
        conn.send(json.dumps(payload))
        LOGGER.debug('SEND: %s', six.text_type(payload))
        recv = json.loads(conn.recv())
        LOGGER.debug('RECV: %s', six.text_type(recv))
        ret = recv['data']
        try:
            ret = json.loads(ret)
        except (TypeError, ValueError):
            pass
        return ret
    except (socket.error, socket.timeout) as ex:
        _handle_error_10042(ex)
    finally:
        conn.close()


def _handle_error_10042(exception):
    if (isinstance(exception, OSError)
            and exception.errno == 10042):
        print("""
This is a bug of websocket-client 0.47.0 with python 3.6.4,
see: https://github.com/websocket-client/websocket-client/issues/404
""")
        raise exception
