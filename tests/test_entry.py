# -*- coding=UTF-8 -*-
"""Test class `cgtwq.Entry`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest

import cgtwq
import util


@pytest.fixture(name='entry')
@util.skip_if_not_logged_in
def _entry():
    cgtwq.DesktopClient().connect()
    return cgtwq.Database('proj_mt').module('shot').select(
        'F950A26F-DD4E-E88B-88EE-9C09EF3F7695').to_entry()


@util.skip_if_not_logged_in
def test_entry_related(entry):
    result = entry.related()
    assert isinstance(result, cgtwq.Selection)
