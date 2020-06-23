# -*- coding=UTF-8 -*-
"""Test `cgtwq.helper.wlf` module.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest

import cgtwq.helper.wlf
from tests import util


@util.skip_if_not_logged_in
def test_get_database():
    assert cgtwq.helper.wlf.get_database_by_file(
        'MT_example.jpg') == 'proj_mt'
    assert cgtwq.helper.wlf.get_database_by_file(
        'MT2_example.jpg') == 'proj_mt2'
    assert cgtwq.helper.wlf.get_database_by_file(
        'JSL_example.jpg') == 'proj_slj'

    with pytest.raises(cgtwq.helper.wlf.DatabaseError):
        cgtwq.helper.wlf.CGTWQHelper.get_database('example.jpg')
