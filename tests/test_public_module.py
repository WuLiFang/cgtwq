# -*- coding=UTF-8 -*-
"""Test module `cgtwq.public_module`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import cgtwq
from util import skip_if_not_logged_in


@skip_if_not_logged_in
def test_select_all():
    cgtwq.DesktopClient().connect()

    cgtwq.ACCOUNT.select_all()
    cgtwq.PROJECT.select_all()


@skip_if_not_logged_in
def test_select_activated():
    cgtwq.DesktopClient().connect()

    cgtwq.ACCOUNT.select_activated()
    cgtwq.PROJECT.select_activated()

    # Backport
    cgtwq.ACCOUNT.all()


@skip_if_not_logged_in
def test_get_public_module_names():
    cgtwq.DesktopClient().connect()

    cgtwq.ACCOUNT.names()
    cgtwq.PROJECT.names()
