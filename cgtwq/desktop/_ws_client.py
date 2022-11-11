# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Text

import websocket
import json

import socket

from contextlib import closing
from .._http_client import JSONEncoder


def _handle_error_10042(exception):
    # type: (Any) -> None
    if isinstance(exception, OSError) and exception.errno == 10042:
        print(
            """
This is a bug of websocket-client 0.47.0 with python 3.6.4,
see: https://github.com/websocket-client/websocket-client/issues/404
"""
        )
        raise exception


class WSClient:
    timeout = 1.0

    def __init__(self, url):
        # type: (Text) -> None
        self._url = url
        self._encoder = JSONEncoder()

    def call(self, controller, method, **kwargs):
        # type: (Text, Text, Any) -> Any
        payload = dict(sign=controller, method=method, **kwargs)
        payload.setdefault("type", "get")
        # XXX: can not reuse connection, second call will not work.
        with closing(websocket.create_connection(self._url, self.timeout)) as conn:  # type: ignore
            try:
                conn.send(self._encoder.encode(payload))  # type: ignore
                recv = json.loads(conn.recv())  # type: ignore
                ret = recv["data"]
                try:
                    ret = json.loads(ret)
                except (TypeError, ValueError):
                    pass
                return ret
            except (socket.error, socket.timeout) as ex:
                _handle_error_10042(ex)

    def call_main_widget(self, method, **kwargs):
        # type: ( Text, Any) -> Any
        return self.call(
            "main_widget",
            method,
            database="main_widget",
            module="main_widget",
            **kwargs
        )
