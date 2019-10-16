# -*- coding=UTF-8 -*-
"""Test `cgtwq.helper.wlf` module.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest

import cgtwq.helper.wlf


def test_get_database():
    assert cgtwq.helper.wlf.CGTWQHelper.get_database(
        'MT_example.jpg') == 'proj_mt'
    assert cgtwq.helper.wlf.CGTWQHelper.get_database(
        'MT2_example.jpg') == 'proj_mt2'

    with pytest.raises(cgtwq.helper.wlf.DatabaseError):
        cgtwq.helper.wlf.CGTWQHelper.get_database('example.jpg')
