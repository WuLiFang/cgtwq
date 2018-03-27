# -*- coding=UTF-8 -*-
"""Test module `cgtwq.database`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import uuid
from unittest import TestCase, main

from util import skip_if_not_logged_in
from cgtwq import database, model
from cgtwq import Filter
import cgtwq


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

    def test_get_pipline(self):
        result = self.database.get_piplines(cgtwq.Filter('name', '合成'))
        self.assertIsInstance(result[0], database.PipelineInfo)

    def test_get_software(self):
        result = self.database.get_software('maya')
        self.assertIsInstance(result, unicode)

    def test_data(self):
        dummy_data = unicode(uuid.uuid4())
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
        self.module = database.Database('proj_big')['shot_task']

    def test_pipeline(self):
        result = self.module.pipelines()
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
        result = cgtwq.PROJECT.names()
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, unicode)


@skip_if_not_logged_in
class AccountTestCase(TestCase):
    def test_names(self):
        result = cgtwq.ACCOUNT.names()
        self.assertIsInstance(result, tuple)
        for i in result:
            self.assertIsInstance(i, unicode)


if __name__ == '__main__':
    main()
