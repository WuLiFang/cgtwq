# -*- coding=UTF-8 -*-
# pylint: disable=invalid-name
"""Test `cgtw.client` module on real server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from unittest import TestCase, main

import cgtwq
import cgtwq.model
from tests import util

pytestmark = [util.skip_if_desktop_client_not_running]


class DesktopClientTestCase(TestCase):
    def test_plugin_data(self):
        try:
            result = cgtwq.DesktopClient().plugin.data()
            self.assertIsInstance(result, cgtwq.model.PluginData)
        except cgtwq.IDError:
            pass

    def test_refresh(self):
        cgtwq.DesktopClient().refresh('proj_sdktest', 'shot')

    def test_refresh_selected(self):
        cgtwq.DesktopClient().refresh_selected('proj_sdktest', 'shot')


def test_current_select():
    try:
        select = cgtwq.DesktopClient().current_select()
        assert isinstance(select, cgtwq.Selection)
    except ValueError as ex:
        if ex.args != ('Empty selection.',):
            raise


if __name__ == '__main__':
    main()
