# -*- coding=UTF-8 -*-
"""Pytest config.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest

import cgtwq


@pytest.fixture(autouse=True, scope='session')
def _connect_desktop_client():
    client = cgtwq.DesktopClient()
    if client.is_logged_in():
        client.connect()
