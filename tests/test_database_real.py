# -*- coding=UTF-8 -*-
# pylint: disable=invalid-name
"""Test module `cgtwq.database`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import random
from unittest import TestCase, main

import pytest
import six

import cgtwq
import cgtwq.model
from cgtwq import Filter, model
from tests import util

pytestmark = [util.skip_if_not_logged_in]


class DataBaseTestCase(TestCase):
    def setUp(self):
        self.database = cgtwq.Database('proj_sdktest')

    def test_get_filebox(self):
        # filters.
        self.database.filebox.filter(cgtwq.Filter('title', '检查MOV'))
        # id
        self.database.filebox.from_id('271')

    def test_get_pipeline(self):
        result = self.database.pipeline.filter(
            cgtwq.Filter('entity_name', '合成'))
        self.assertIsInstance(result[0], cgtwq.model.PipelineInfo)


class ModuleTestCase(TestCase):
    def setUp(self):
        self.module = cgtwq.Database('proj_sdktest').module('shot')

    def test_pipeline(self):
        result = self.module.pipelines()
        assert result
        for i in result:
            self.assertIsInstance(i, cgtwq.model.PipelineInfo)

    def test_get_history(self):

        result = self.module.history.filter(Filter('status', 'Approve'))
        for i in result:
            assert isinstance(i, model.HistoryInfo)

    def test_count_history(self):

        result = self.module.history.count(Filter('status', 'Approve'))
        self.assertIsInstance(result, int)


class ProjectTestCase(TestCase):
    def test_names(self):
        result = cgtwq.PROJECT.names()
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, six.text_type)


class AccountTestCase(TestCase):
    def test_names(self):
        result = cgtwq.ACCOUNT.names()
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, six.text_type)


@pytest.fixture(name='database')
def _database():
    return cgtwq.Database('proj_sdktest')


def test_get_software(database):
    assert isinstance(database, cgtwq.Database)
    path = database.software.get_path('maya')
    assert isinstance(path, six.text_type)


def test_database_modules(database):
    result = database.filter()
    assert all(isinstance(i, cgtwq.Module) for i in result)


def test_database_fields(database):
    # Get
    assert isinstance(database, cgtwq.Database)
    result = database.field.filter()
    assert all(isinstance(i, cgtwq.model.FieldMeta) for i in result)
    result = database.field.filter_one(cgtwq.Field('sign') == 'shot.shot')
    assert isinstance(result, cgtwq.model.FieldMeta)

    # Create
    field_sign = 'task.python_test_{}'.format(
        ''.join([random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(20)]))
    database.field.create(sign=field_sign, type_='int')

    # Delete
    field = database.field.filter_one(cgtwq.Field('sign') == field_sign)
    assert field.sign == field_sign
    database.field.delete(field.id)


def test_database_filebox(database):
    result = database.filebox.filter()
    assert all(isinstance(i, cgtwq.model.FileBoxMeta) for i in result)
    result = database.filebox.filter(cgtwq.Field('title') == '检查MOV')
    result = database.filebox.from_id('271')


def test_database_software(database):
    assert isinstance(database, cgtwq.Database)
    result = database.software.get_path('maya')
    assert isinstance(result, six.text_type)
    result = database.software.get_path_from_type('maya')
    assert isinstance(result, six.text_type)


if __name__ == '__main__':
    main()
