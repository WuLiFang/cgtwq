# -*- coding=UTF-8 -*-
"""Test module `cgtwq.database`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import uuid
from unittest import TestCase, main

import pytest
import six

import cgtwq
import cgtwq.database
import cgtwq.model
import util
from util import skip_if_not_logged_in

database = cgtwq.database  # pylint: disable=invalid-name
model = cgtwq.model  # pylint: disable=invalid-name


@skip_if_not_logged_in
class SelectionTestCase(TestCase):
    def setUp(self):
        cgtwq.update_setting()
        module = database.Database('proj_big').module('shot')
        select = module.filter(cgtwq.Filter('flow_name', '合成') &
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
            try:
                path = i.get_image().path
                i.set_image(path)
            except ValueError:
                path = util.path('resource', 'gray.png')
            i.set_image(path)

    def test_get_notes(self):
        result = self.select.notify.get()
        for i in result:
            self.assertIsInstance(i, model.NoteInfo)

    def test_send_message(self):
        self.select.notify.send('test',
                                'test <b>message</b>',
                                cgtwq.util.current_account_id())

    def test_get_filebox_submit(self):
        select = self.select
        result = select.filebox.get_submit()
        self.assertIsInstance(result, cgtwq.model.FileBoxInfo)

    def test_has_permission_on_status(self):
        select = self.select
        result = select.has_permission_on_status('artist')
        self.assertIsInstance(result, bool)


@pytest.fixture(name='select')
@skip_if_not_logged_in
def _select():
    cgtwq.update_setting()
    return cgtwq.Database('proj_mt').module('shot').select(
        'F950A26F-DD4E-E88B-88EE-9C09EF3F7695')


logging.basicConfig(level=10)


@skip_if_not_logged_in
def test_flow(select):
    for i in ('leader_status', 'director_status', 'client_status'):
        try:
            select.flow.approve(i, 'test approve')
            assert select[i] == ('Approve',)
            select.flow.retake(i, 'test retake')
            assert select[i] == ('Retake',)
            select.flow.close(i, 'test close')
            assert select[i] == ('Close',)
        except cgtwq.PermissionError:
            continue


@skip_if_not_logged_in
def test_flow_submit(select):
    select.flow.submit(message='test submit')
    # TODO:Remove below test at next major version.
    select.submit(note='test submit old')


@skip_if_not_logged_in
def test_flow_assign(select):
    accounts = [cgtwq.account.get_account_id(
        cgtwq.core.CONFIG['DEFAULT_TOKEN'])]
    select.flow.assign(accounts)


@skip_if_not_logged_in
def test_history(select):

    # Count
    result = select.history.count()
    assert isinstance(result, int)
    # Get
    result = select.history.get()
    for i in result:
        assert isinstance(i, model.HistoryInfo)
        assert isinstance(i.text, cgtwq.Message)

    # Undo
    select.flow.close('leader_status')
    select.flow.retake('leader_status')
    select.history.undo(select.history.get()[-1])
    assert select['leader_status'][0] == 'Close'


@skip_if_not_logged_in
def test_note(select):
    assert isinstance(select, cgtwq.Selection)
    note_message = 'TEST-{}'.format(uuid.uuid4().hex)
    select.notify.add(note_message)
    notes = select.notify.get()
    note = None
    for i in notes:
        assert isinstance(i, cgtwq.model.NoteInfo)
        if i.message == note_message:
            note = i
    assert note
    select.notify.delete(note.id)
    assert list(set(notes).difference(select.notify.get()))[0] is note


@skip_if_not_logged_in
def test_selection_count(select):
    result = select.count(cgtwq.Field('shot.shot').has('_sc001'))
    assert isinstance(result, int)


@skip_if_not_logged_in
def test_selection_distinct(select):
    result = select.distinct(cgtwq.Field('shot.shot').has('_sc001'))
    assert isinstance(result, tuple)


@skip_if_not_logged_in
def test_selection_pipeline(select):
    result = select.pipeline.all()
    assert result
    assert all(isinstance(i, cgtwq.model.PipelineInfo) for i in result)

    result = select.to_entries()[0].pipeline.one()
    assert isinstance(result, cgtwq.model.PipelineInfo)


@skip_if_not_logged_in
def test_selection_folder(select):
    result = select.folder.all()
    assert isinstance(result, list)

    result = select.folder.from_sign('comp_image')
    assert isinstance(result, dict), type(result)
    assert set(result.keys()) == set(select)
    assert all(isinstance(i, list) for i in result.values())


if __name__ == '__main__':
    main()
