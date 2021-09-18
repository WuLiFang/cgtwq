# -*- coding=UTF-8 -*-
"""Test module `cgtwq.database`. with a mocked environment.  """

from __future__ import absolute_import, division, print_function, unicode_literals

from unittest import TestCase, main

import six

import cgtwq

if six.PY3:
    from unittest.mock import (
        MagicMock,
        patch,
    )  # pylint: disable=import-error,no-name-in-module
else:
    from mock import MagicMock, patch


class DatabaseTestCase(TestCase):
    def test_getitem(self):
        database = cgtwq.Database("dummy_db")
        self.assertEqual(database.name, "dummy_db")
        result = database["shot"]
        self.assertIsInstance(result, cgtwq.Module)
        self.assertEqual(result.name, "shot")


class ModuleTestCase(TestCase):
    def setUp(self):
        patcher = patch("cgtwq.server.call")
        self.addCleanup(patcher.stop)
        self.call_method = patcher.start()

        for i in (
            patch("cgtwq.DesktopClient.server_ip"),
            patch("cgtwq.DesktopClient.token"),
        ):
            self.addCleanup(i.stop)
            i.start()

        self.module = cgtwq.Database("dummy_db")["shot"]

    def test_select(self):
        module = self.module
        result = module.select("0")
        self.assertIsInstance(result, cgtwq.Selection)
        last = result
        result = module["0"]
        self.assertIsInstance(result, cgtwq.Selection)
        self.assertEqual(result, last)

        self.call_method.assert_not_called()

    def test_filter(self):
        module = self.module
        method = self.call_method
        dummy_resp = ["0", "1"]
        method.return_value = dummy_resp

        select = module.filter(cgtwq.Filter("key", "value"))
        method.assert_called_with(
            "c_orm",
            "get_with_filter",
            db="dummy_db",
            module="shot",
            module_type="task",
            sign_array=("task.id",),
            sign_filter_array=[["task.key", "=", "value"]],
            token=select.token,
        )
        self.assertIsInstance(select, cgtwq.Selection)

    @patch("cgtwq.Module.filter")
    @patch("cgtwq.Module.select")
    def test_getitem(self, select, filter_):
        assert isinstance(select, MagicMock)
        assert isinstance(filter_, MagicMock)
        module = self.module
        select.return_value = filter_.return_value = cgtwq.Selection(module, "random")

        _ = module["abc"]
        select.assert_called_once_with("abc")
        filters = cgtwq.Filter("dce", "fgh")
        _ = module[filters]
        filter_.assert_called_once_with(filters)


if __name__ == "__main__":
    main()
