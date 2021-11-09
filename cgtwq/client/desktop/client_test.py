# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import absolute_import, division, print_function, unicode_literals


from . import client
from ... import _test


@_test.skip_if_ci
def test_config_path():
    assert client.DesktopClient.config_path()


@_test.skip_if_ci
def test_default_socket_url():
    c = client.DesktopClient()
    assert c.socket_url
    # assert c.socket_url == "ws://127.0.0.1:64995"
