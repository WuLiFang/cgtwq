# -*- coding=UTF-8 -*-
"""Test `cgtw.client` module on real server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from unittest import TestCase, main, skip

import cgtwq
from util import skip_if_not_logged_in


@skip_if_not_logged_in
class CGTeamWorkClientTestCase(TestCase):
    def test_plugin_data(self):
        try:
            result = cgtwq.CGTeamWorkClient.get_plugin_data()
            self.assertIsInstance(result, cgtwq.client.PluginData)
        except cgtwq.IDError:
            pass

    def test_status(self):
        result = cgtwq.CGTeamWorkClient().status
        self.assertIsInstance(result, cgtwq.client.CGTeamWorkClientStatus)

    def test_refresh(self):
        cgtwq.CGTeamWorkClient.refresh('proj_big', 'shot_task')

    def test_refresh_selected(self):
        cgtwq.CGTeamWorkClient.refresh_select('proj_big', 'shot_task')


if __name__ == '__main__':
    main()
