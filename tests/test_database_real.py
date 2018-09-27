# -*- coding=UTF-8 -*-
"""Test module `cgtwq.database`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import random
import uuid
from unittest import TestCase, main

import pytest
import six

import cgtwq
from cgtwq import Filter, model
from util import skip_if_not_logged_in


@skip_if_not_logged_in
class DataBaseTestCase(TestCase):
    def setUp(self):
        cgtwq.update_setting()
        self.database = cgtwq.Database('proj_big')

    def test_get_filebox(self):
        # filters.
        self.database.get_fileboxes(filters=cgtwq.Filter('title', '检查MOV'))
        # id
        self.database.get_fileboxes(id_='271')

    def test_get_pipeline(self):
        result = self.database.get_pipelines(cgtwq.Filter('entity_name', '合成'))
        self.assertIsInstance(result[0], cgtwq.model.PipelineInfo)

    def test_data(self):
        dummy_data = six.text_type(uuid.uuid4())
        key = '_test_temp'
        self.database.set_data(key, dummy_data)
        result = self.database.get_data(key)
        self.assertEqual(result, dummy_data)
        result = self.database.get_data(key, False)
        self.assertNotEqual(result, dummy_data)
        self.database.set_data(key, dummy_data, False)
        result = self.database.get_data(key, False)
        self.assertEqual(result, dummy_data)


@skip_if_not_logged_in
class ModuleTestCase(TestCase):
    def setUp(self):
        cgtwq.update_setting()
        self.module = cgtwq.Database('proj_big').module('shot')

    def test_pipeline(self):
        result = self.module.pipelines()
        assert result
        for i in result:
            self.assertIsInstance(i, cgtwq.model.PipelineInfo)

    def test_get_history(self):

        result = self.module.get_history(Filter('status', 'Approve'))
        for i in result:
            assert isinstance(i, model.HistoryInfo)

    def test_count_history(self):

        result = self.module.count_history(Filter('status', 'Approve'))
        self.assertIsInstance(result, int)


@skip_if_not_logged_in
class ProjectTestCase(TestCase):
    def test_names(self):
        cgtwq.update_setting()
        result = cgtwq.PROJECT.names()
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, six.text_type)


@skip_if_not_logged_in
class AccountTestCase(TestCase):
    def test_names(self):
        cgtwq.update_setting()
        result = cgtwq.ACCOUNT.names()
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, six.text_type)


@pytest.fixture(name='database')
@skip_if_not_logged_in
def _database():
    cgtwq.update_setting()
    return cgtwq.Database('proj_mt')


@skip_if_not_logged_in
def test_get_software(database):
    assert isinstance(database, cgtwq.Database)
    path = database.get_software('maya')
    assert isinstance(path, six.text_type)


@skip_if_not_logged_in
def test_database_modules(database):
    result = database.modules()
    assert all(isinstance(i, cgtwq.Module) for i in result)


@skip_if_not_logged_in
def test_database_fields(database):
    # Get
    result = database.get_fields()
    assert all(isinstance(i, cgtwq.model.FieldInfo) for i in result)
    result = database.get_field(cgtwq.Field('sign') == 'shot.shot')
    assert isinstance(result, cgtwq.model.FieldInfo)

    # Create
    field_sign = 'task.python_test_{}'.format(
        ''.join([random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(20)]))
    database.create_field(sign=field_sign, type_='int')

    # Delete
    field = database.get_field(cgtwq.Field('sign') == field_sign)
    database.delete_field(field.id)


@skip_if_not_logged_in
def test_database_filebox(database):
    result = database.filebox.filter()
    assert all(isinstance(i, cgtwq.model.FileBoxMeta) for i in result)
    result = database.filebox.filter(cgtwq.Field('title') == '检查MOV')
    result = database.filebox.get('271')


if __name__ == '__main__':
    main()
