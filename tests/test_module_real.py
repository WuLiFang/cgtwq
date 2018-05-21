# -*- coding=UTF-8 -*-
"""Test module `cgtwq.database`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest

import cgtwq
import util


@pytest.fixture(name='module')
@util.skip_if_not_logged_in
def _module():
    cgtwq.update_setting()
    return cgtwq.Database('proj_mt').module('shot_task')


@util.skip_if_not_logged_in
def test_module_fileds(module):
    result = module.fields()
    print(result)


@util.skip_if_not_logged_in
def test_module_flow(module):
    result = module.flow()
    print(result)


@util.skip_if_not_logged_in
def test_module_pipeline(module):
    result = module.pipelines()
    print(result)
