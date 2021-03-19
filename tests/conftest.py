# -*- coding=UTF-8 -*-
"""Pytest config.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

import pytest

import cgtwq
import cgtwq.core


@pytest.fixture(autouse=True, scope='session')
def _connect_desktop_client():
    account, passwd = (os.getenv('CGTWQ_TEST_ACCOUNT'),
                       os.getenv('CGTWQ_TEST_PASSWORD'))
    if account and passwd:
        info = cgtwq.login(account, passwd)
        cgtwq.core.CONFIG['DEFAULT_TOKEN'] = info.token
        return

    client = cgtwq.DesktopClient()
    if client.is_logged_in():
        client.connect()
