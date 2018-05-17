# -*- coding=UTF-8 -*-
"""Test module `cgtwq.database`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import uuid
from unittest import TestCase, main

import six

import cgtwq
from cgtwq import database, model
from util import skip_if_not_logged_in


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
        result = select.get_folder('comp_image')
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)
        self.assertRaises(ValueError,
                          select.get_folder,
                          six.text_type(uuid.uuid4()))

    def test_get_filebox(self):
        select = self.select
        result = select.filebox.get('submit')
        self.assertIsInstance(result, model.FileBoxInfo)

        # Test wrong sign.
        self.assertRaises(ValueError,
                          select.filebox.get,
                          six.text_type(uuid.uuid4()))

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
        result = self.select.notify.get()
        for i in result:
            self.assertIsInstance(i, model.NoteInfo)

    def test_send_message(self):
        self.select.notify.send('test',
                                'test <b>message</b>',
                                cgtwq.util.current_account_id())

    def test_get_history(self):
        result = self.select.history.get()
        for i in result:
            assert isinstance(i, model.HistoryInfo)

    def test_count_history(self):
        result = self.select.history.count()
        self.assertIsInstance(result, int)

    def test_add_note(self):
        select = self.select
        select.notify.add('test', cgtwq.util.current_account_id())

    def test_get_filebox_submit(self):
        select = self.select
        result = select.filebox.get_submit()
        self.assertIsInstance(result, cgtwq.model.FileBoxInfo)


if __name__ == '__main__':
    main()
