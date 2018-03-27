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
class SelectionTestCase(TestCase):
    def setUp(self):
        cgtwq.update_setting()
        module = database.Database('proj_big')['shot_task']
        select = module.filter(cgtwq.Filter('pipeline', '合成') &
                               cgtwq.Filter('shot.shot',
                                            ['SNJYW_EP26_06_sc349', 'SNJYW_EP26_06_sc350']))
        assert isinstance(select, cgtwq.Selection)
        if not select:
            raise ValueError('No selection to test.')
        self.assertEqual(len(select), 2)
        self.select = select

    def test_get_dir(self):
        select = self.select
        result = select.get_path('comp_image')
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)
        self.assertRaises(ValueError,
                          select.get_filebox,
                          unicode(uuid.uuid4()))

    def test_get_filebox(self):
        select = self.select
        result = select.get_filebox('submit')
        self.assertIsInstance(result, model.FileBoxDetail)

        # Test wrong sign.
        self.assertRaises(ValueError,
                          select.get_filebox,
                          unicode(uuid.uuid4()))

    def test_get_fields(self):
        result = self.select.get_fields('id', 'shot.shot')
        for i in result:
            self.assertEqual(len(i), 2)

    def test_get_image(self):
        result = self.select.get_image('image')
        for i in result:
            self.assertIsInstance(i, model.ImageInfo)

    def test_set_image(self):
        for i in self.select.to_entries():
            assert isinstance(i, cgtwq.Entry)
            path = i.get_image().path
            i.set_image(path)

    def test_get_notes(self):
        result = self.select.get_notes()
        for i in result:
            self.assertIsInstance(i, model.NoteInfo)

    def test_send_message(self):
        self.select.send_message('test',
                                 'test <b>message</b>',
                                 cgtwq.get_account_id(cgtwq.DesktopClient.token()))

    def test_get_history(self):
        result = self.select.get_history()
        for i in result:
            assert isinstance(i, model.HistoryInfo)

    def test_count_history(self):
        result = self.select.count_history()
        self.assertIsInstance(result, int)


class TaskTestCase(TestCase):
    def test_get_note(self):
        pass


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
