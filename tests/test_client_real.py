# -*- coding=UTF-8 -*-
"""Test `cgtw.client` module on real server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from unittest import TestCase, main

import cgtwq
from util import skip_if_not_logged_in


@skip_if_not_logged_in
class DesktopClientTestCase(TestCase):
    def test_plugin_data(self):
        try:
            result = cgtwq.DesktopClient().get_plugin_data()
            self.assertIsInstance(result, cgtwq.model.PluginData)
        except cgtwq.IDError:
            pass

    def test_refresh(self):
        cgtwq.DesktopClient().refresh('proj_big', 'shot')

    def test_refresh_selected(self):
        cgtwq.DesktopClient().refresh_selected('proj_big', 'shot')


@skip_if_not_logged_in
def test_current_select():
    select = cgtwq.DesktopClient().current_select()
    assert isinstance(select, cgtwq.Selection)


if __name__ == '__main__':
    main()
