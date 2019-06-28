# -*- coding=UTF-8 -*-
"""Test module `cgtwq.public_module`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import cgtwq
from tests import util


@util.skip_if_not_logged_in
def test_select_all():

    cgtwq.ACCOUNT.select_all()
    cgtwq.PROJECT.select_all()


@util.skip_if_not_logged_in
def test_select_activated():

    cgtwq.ACCOUNT.select_activated()
    cgtwq.PROJECT.select_activated()

    # TODO: Backport, remove this as next major version.
    cgtwq.ACCOUNT.all()


@util.skip_if_not_logged_in
def test_get_public_module_names():

    cgtwq.ACCOUNT.names()
    cgtwq.PROJECT.names()
