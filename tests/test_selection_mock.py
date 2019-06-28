# -*- coding=UTF-8 -*-
# pylint: disable=invalid-name
"""Test module `cgtwq.selection`."""


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest

import cgtwq


def test_empty_selection():
    with pytest.raises(cgtwq.EmptySelection):
        cgtwq.Selection(cgtwq.Database('').module(''))
    assert issubclass(cgtwq.EmptySelection, ValueError)
