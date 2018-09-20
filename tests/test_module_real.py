# -*- coding=UTF-8 -*-
"""Test module `cgtwq.database`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import random
import string

import pytest

import cgtwq
import util


@pytest.fixture(name='module')
@util.skip_if_not_logged_in
def _module():
    cgtwq.update_setting()
    return cgtwq.Database('proj_mt').module('shot')


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


@util.skip_if_not_logged_in
def test_module_field(module):
    field_sign = 'python_test_{}'.format(
        ''.join([random.choice(string.letters) for i in range(20)]))
    module.create_field(sign=field_sign, type_='int')
    field = next(i for i in module.fields()
                 if i.sign == module.field(field_sign))
    module.delete_field(field.id)
