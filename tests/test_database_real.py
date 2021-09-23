# -*- coding=UTF-8 -*-
# pylint: disable=invalid-name
# pyright: reportUnknownParameterType=none
"""Test module `cgtwq.database`."""

from __future__ import absolute_import, division, print_function, unicode_literals

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
        self.database = cgtwq.Database("proj_sdktest")

    def test_get_pipeline(self):
        result = self.database.pipeline.filter(cgtwq.Filter("entity", "合成"))
        self.assertIsInstance(result[0], cgtwq.model.PipelineInfo)


def test_list_filebox_by_pipeline():
    db = cgtwq.Database("proj_sdktest")
    (pipeline,) = db.pipeline.filter(cgtwq.Field("entity") == "合成")
    pipeline.module
    filebox_list = db.filebox.list_by_pipeline(pipeline)
    assert filebox_list


class ModuleTestCase(TestCase):
    def setUp(self):
        self.module = cgtwq.Database("proj_sdktest").module("shot")

    def test_pipeline(self):
        result = self.module.pipelines()
        assert len(result) > 0
        for i in result:
            self.assertIsInstance(i, cgtwq.model.PipelineInfo)

    def test_get_history(self):

        result = self.module.history.filter(Filter("status", "Approve"))
        for i in result:
            assert isinstance(i, model.HistoryInfo)
            assert i.id
            assert i.account_id
            assert i.task_id
            assert i.time

    def test_count_history(self):

        result = self.module.history.count(Filter("status", "Approve"))
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


@pytest.fixture(name="database")
def _database():
    return cgtwq.Database("proj_sdktest")


def test_get_software(database):
    assert isinstance(database, cgtwq.Database)
    path = database.software.get_path("maya")
    assert isinstance(path, six.text_type)


def test_database_modules(database):
    result = database.filter()
    assert all(isinstance(i, cgtwq.Module) for i in result)


def test_database_fields(database):
    # Get
    assert isinstance(database, cgtwq.Database)
    result = database.field.filter()
    assert all(isinstance(i, cgtwq.model.FieldMeta) for i in result)
    result = database.field.filter_one(
        cgtwq.Field("sign") == cgtwq.compat.adapt_field_sign("shot.entity")
    )
    assert isinstance(result, cgtwq.model.FieldMeta)

    # Create
    field_sign = "task.python_test_{}".format(
        "".join(
            [
                random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
                for _ in range(20)
            ]
        )
    )
    database.field.create(sign=field_sign, type_="int")

    # Delete
    field = database.field.filter_one(cgtwq.Field("sign") == field_sign)
    assert field.sign == field_sign
    database.field.delete(field.id)

@util.skip_for_cgteamwork6
def test_database_filebox(database):
    result = database.filebox.filter()
    assert all(isinstance(i, cgtwq.model.FileBoxMeta) for i in result)
    result = database.filebox.filter(cgtwq.Field("title") == "检查MOV")
    result = database.filebox.from_id("271")


def test_database_software(database):
    assert isinstance(database, cgtwq.Database)
    result = database.software.get_path("maya")
    assert isinstance(result, six.text_type)
    result = database.software.get_path_from_type("maya")
    assert isinstance(result, six.text_type)


if __name__ == "__main__":
    main()
