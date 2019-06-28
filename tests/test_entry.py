# -*- coding=UTF-8 -*-
"""Test class `cgtwq.Entry`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest

import cgtwq
from tests import util


@pytest.fixture(name='entry')
@util.skip_if_not_logged_in
def _entry():
    return cgtwq.Database('proj_sdktest').module('shot').select(
        'D84AF30B-89FD-D06D-349A-F01F5D99744C').to_entry()


@util.skip_if_not_logged_in
def test_entry_related(entry):
    assert isinstance(entry, cgtwq.Entry)
    result = entry.related()
    assert isinstance(result, cgtwq.Selection)
