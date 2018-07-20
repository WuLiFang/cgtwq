# -*- coding=UTF-8 -*-
"""Test module `cgtwq.database`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import uuid
from unittest import TestCase, main

import six

import cgtwq
from cgtwq import Filter, database, model
from util import skip_if_not_logged_in


@skip_if_not_logged_in
class DataBaseTestCase(TestCase):
    def setUp(self):
        cgtwq.update_setting()
        self.database = database.Database('proj_big')

    def test_get_filebox(self):
        # filters.
        self.database.get_fileboxes(filters=cgtwq.Filter('title', '检查MOV'))
        # id
        self.database.get_fileboxes(id_='271')

    def test_get_pipeline(self):
        result = self.database.get_pipelines(cgtwq.Filter('entity_name', '合成'))
        self.assertIsInstance(result[0], database.PipelineInfo)

    def test_get_software(self):
        result = self.database.get_software('maya')
        self.assertIsInstance(result, six.text_type)

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
        self.module = database.Database('proj_big').module('shot')

    def test_pipeline(self):
        result = self.module.pipelines()
        assert result
        for i in result:
            self.assertIsInstance(i, database.PipelineInfo)

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


if __name__ == '__main__':
    main()
