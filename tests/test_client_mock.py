# -*- coding=UTF-8 -*-
"""Test module `cgtwq.client`. with a mocked client.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import os
import socket
import uuid
from functools import partial
from unittest import TestCase, main, skip

import six

import cgtwq

if six.PY3:
    from unittest.mock import patch  # pylint: disable=import-error,no-name-in-module
else:
    from mock import patch


# Same argument with json.dumps used in `DesktopClient().call`.
dumps = partial(json.dumps, sort_keys=True, indent=4)


def server_dumps(code, data):
    """CGTeamwork server dumps json in this style.  """

    return dumps({'code': six.text_type(code), 'data': data})


class DesktopClientTestCase(TestCase):
    def setUp(self):
        patcher = patch('cgtwq.client.create_connection')
        self.addCleanup(patcher.stop)
        self.create_connection = patcher.start()
        self.conn = self.create_connection.return_value

    def test_is_running(self):
        conn = self.conn

        # Logged in.
        conn.recv.return_value = server_dumps(1, six.text_type(uuid.uuid4()))
        result = cgtwq.DesktopClient().is_running()
        self.assertIs(result, True)
        conn.send.assert_called_once_with(
            dumps({
                'sign': 'main_widget',
                'method': 'get_token',
                'database': 'main_widget',
                'module': 'main_widget',
                'type': 'get'}
            )
        )

        # Running but not logged in.
        conn.recv.return_value = server_dumps(1, True)
        result = cgtwq.DesktopClient().is_running()
        self.assertIs(result, True)

        # Not running.
        conn.recv.side_effect = socket.timeout
        result = cgtwq.DesktopClient().is_running()
        self.assertIs(result, False)

    def test_is_logged_in(self):
        conn = self.conn

        # Logged in.
        conn.recv.return_value = server_dumps(
            1, six.text_type(uuid.uuid4()))
        result = cgtwq.DesktopClient().is_logged_in()
        self.assertIs(result, True)
        conn.send.assert_called_once_with(
            dumps({
                'sign': 'main_widget',
                'method': 'get_token',
                'database': 'main_widget',
                'module': 'main_widget',
                'type': 'get'}
            )
        )

        # Running but not logged in.
        conn.recv.return_value = server_dumps(1, True)
        result = cgtwq.DesktopClient().is_logged_in()
        self.assertIs(result, False)

        # Not running.
        conn.recv.side_effect = socket.timeout
        result = cgtwq.DesktopClient().is_logged_in()
        self.assertIs(result, False)

    def test_executable(self):
        result = cgtwq.DesktopClient().executable()
        if result is not None:
            self.assertIsInstance(result, (six.text_type))
        self.conn.assert_not_called()

    def test_start(self):
        conn = self.conn
        conn.recv.return_value = server_dumps(1, True)
        cgtwq.DesktopClient().start()
        if cgtwq.DesktopClient().executable():
            self.conn.send.assert_called_once()

    def test_refresh(self):
        conn = self.conn
        conn.recv.return_value = server_dumps(1, True)
        cgtwq.DesktopClient().refresh('proj_big', 'shot')
        conn.send.assert_called_once_with(
            dumps({
                'sign': 'view_control',
                'method': 'refresh',
                'database': 'proj_big',
                'module': 'shot',
                'type': 'send'}))

    def test_refresh_selected(self):
        conn = self.conn
        conn.recv.return_value = server_dumps(1, True)
        cgtwq.DesktopClient().refresh_selected('proj_big', 'shot')
        conn.send.assert_called_once_with(
            dumps({
                'sign': 'view_control',
                'method': 'refresh_select',
                'database': 'proj_big',
                'module': 'shot',
                'type': 'send'}))

    def test_token(self):
        conn = self.conn
        uuid_ = six.text_type(uuid.uuid4())
        conn.recv.return_value = server_dumps(1, uuid_)

        # pylint: disable=protected-access
        # Logged in.
        cgtwq.DesktopClient()._token()
        conn.send.assert_called_once_with(
            dumps({
                'sign': 'main_widget',
                'method': 'get_token',
                'database': 'main_widget',
                'module': 'main_widget',
                'type': 'get'})
        )

        result = cgtwq.DesktopClient()._token()
        self.assertEqual(result, uuid_)

        # Running but not logged in.
        conn.recv.return_value = server_dumps(1, True)
        result = cgtwq.DesktopClient()._token()
        self.assertEqual(result, '')

        # Not running.
        self.create_connection.side_effect = socket.timeout
        self.assertRaises(socket.timeout, cgtwq.DesktopClient()._token)

    def test_server_ip(self):
        # pylint: disable=protected-access
        dummy_ip = '192.168.55.55'
        conn = self.conn
        conn.recv.return_value = server_dumps(1, dummy_ip)
        result = cgtwq.DesktopClient()._server_ip()
        conn.send.assert_called_once_with(
            dumps(
                {
                    'sign': 'main_widget',
                    'method': 'get_server_ip',
                    'database': 'main_widget',
                    'module': 'main_widget',
                    'type': 'get'
                }
            )
        )
        self.assertEqual(result, dummy_ip)

    def test_server_http(self):
        dummy_http = '192.168.55.55'
        conn = self.conn
        conn.recv.return_value = server_dumps(1, dummy_http)
        result = cgtwq.DesktopClient().server_http()
        conn.send.assert_called_once_with(
            dumps(
                {
                    'sign': 'main_widget',
                    'method': 'get_server_http',
                    'database': 'main_widget',
                    'module': 'main_widget',
                    'type': 'get'
                }
            )
        )
        self.assertEqual(result, dummy_http)

    def test_plugin_data(self):
        dummy_data = {'id_list': ['1', '2']}
        uuid_ = six.text_type(uuid.uuid4())
        conn = self.conn
        conn.recv.return_value = server_dumps(1, dummy_data)
        result = cgtwq.DesktopClient().get_plugin_data(uuid_)
        dummy_data2 = dict.fromkeys(cgtwq.client.PluginData._fields)
        dummy_data2.update(dummy_data)
        self.assertEqual(result,
                         cgtwq.client.PluginData(**dummy_data2))
        conn.send.assert_called_once_with(
            dumps(
                {
                    'sign': 'main_widget',
                    'method': 'get_plugin_data',
                    'database': 'main_widget',
                    'module': 'main_widget',
                    'type': 'get',
                    'plugin_uuid': uuid_,
                }
            )
        )

    def test_send_plugin_result(self):
        uuid_ = six.text_type(uuid.uuid4())
        conn = self.conn

        conn.recv.return_value = server_dumps(1, True)
        cgtwq.DesktopClient().send_plugin_result(uuid_)
        conn.send.assert_called_once_with(
            dumps(
                {
                    "method": "exec_plugin_result",
                    "result": False,
                    "database": "main_widget",
                    "sign": "main_widget",
                    "type": "send",
                    "module": "main_widget",
                    "uuid": uuid_
                }
            )
        )


if __name__ == '__main__':
    main()
