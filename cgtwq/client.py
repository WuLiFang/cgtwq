# -*- coding=UTF-8 -*-
"""Get information from CGTeamWork GUI client.  """

from __future__ import absolute_import, print_function, unicode_literals

import json
import logging
import os
import socket
from functools import partial
from subprocess import Popen

from six import text_type
from websocket import create_connection

from wlf.decorators import deprecated

from . import core
from .exceptions import IDError
from .model import PluginData
from .selection import Selection

LOGGER = logging.getLogger(__name__)


class DesktopClient(core.CachedFunctionMixin):
    """Communicate with a CGTeamWork offical GUI clients.  """

    def __init__(self, socket_url=None):
        super(DesktopClient, self).__init__()
        self.socket_url = socket_url or core.CONFIG['DESKTOP_CLIENT_SOCKET_URL']

    def connect(self):
        """Update module config from desktop client.  """

        core.CONFIG['SERVER_IP'] = self.server_ip()
        core.CONFIG['DEFAULT_TOKEN'] = self.token()

    @staticmethod
    def executable():
        """Get a cgteawmwork client executable.

        Returns:
            text_type: Executable path.
        """

        # Get client executable.
        try:
            import cgtw
            executable = os.path.abspath(os.path.join(
                cgtw.__file__, '../../cgtw/CgTeamWork.exe'))
        except ImportError:
            # Try use default when sys.path not been set correctly.
            executable = "C:/cgteamwork/bin/cgtw/CgTeamWork.exe"

        if not os.path.exists(executable):
            executable = None
        return executable

    def start(self):
        """Start client if not running.  """

        executable = self.executable()
        if executable and not self.is_running():
            Popen(executable,
                  cwd=os.path.dirname(executable),
                  close_fds=True)

    def is_running(self):
        """Check if client is running.

        Returns:
            bool: Ture if client is running.
        """

        try:
            self.token(-1)
            return True
        except (socket.error, socket.timeout) as ex:
            _handle_error_10042(ex)

        return False

    def is_logged_in(self):
        """Check if client is logged in.

        Returns:
            bool: True if client is logged in.
        """

        try:
            if self.token(-1):
                return True
        except (socket.error, socket.timeout) as ex:
            _handle_error_10042(ex)
        return False

    def _refresh(self, database, module, is_selected_only):
        self.call('view_control',
                  'refresh_select' if is_selected_only else 'refresh',
                  module=module,
                  database=database,
                  type='send')

    def refresh(self, database, module):
        """
        Refresh specified view in client
        if matched view is opened.

        Args:
            database (text_type): Database of view.
            module (text_type): Module of view.
        """

        self._refresh(database, module, False)

    def refresh_selected(self, database, module):
        """
        Refresh selected part of specified view in client
        if matched view is opened.

        Args:
            database (text_type): Database of view.
            module (text_type): Module of view.
        """

        self._refresh(database, module, True)

    def token(self, max_age=2):
        """Cached client token.  """

        return self._cached('token', self._token, max_age)

    def _token(self):
        """Client token.  """

        ret = self.call_main_widget("get_token")
        if ret is True:
            return ''
        assert isinstance(ret, text_type), type(ret)
        return text_type(ret)

    def server_ip(self, max_age=5):
        """Cached server ip.  """

        return self._cached('server_ip', self._server_ip, max_age)

    def _server_ip(self):
        """Server ip current using by client.  """

        return _get_typed_data(self.call_main_widget("get_server_ip"), text_type)

    def server_http(self):
        """Server http current using by client.  """

        return _get_typed_data(self.call_main_widget("get_server_http"), text_type)

    def get_plugin_data(self, uuid=''):
        """Get plugin data for uuid.

        Args:
            uuid (text_type): Plugin uuid.
        """

        data = self.call_main_widget("get_plugin_data", plugin_uuid=uuid)
        if not data:
            msg = 'No matched plugin'
            if uuid:
                msg += ': {}'.format(uuid)
            msg += '.'
            raise IDError(msg)
        assert isinstance(data, dict), type(data)
        for i in PluginData._fields:
            data.setdefault(i, None)
        return PluginData(**data)

    def selection(self):
        """Get current selection from client.

        Returns:
            Selection: Current selection.
        """

        plugin_data = self.get_plugin_data()
        return Selection.from_data(**plugin_data._asdict())

    current_select = deprecated(
        selection, reason='Use `Desktop.selection` instead.')

    def send_plugin_result(self, uuid, result=False):
        """
        Tell client plugin execution result.
        if result is `False`, following operation will been abort.

        Args:
            uuid (text_type): Plugin uuid.
            result (bool, optional): Defaults to False. Plugin execution result.
        """

        self.call_main_widget("exec_plugin_result",
                              uuid=uuid,
                              result=result,
                              type='send')

    def call_main_widget(self, *args, **kwargs):
        """Send data to main widget.

        Args:
            **data (dict): Data to send.

        Returns:
            dict or text_type: Recived data.
        """

        method = partial(
            self.call, "main_widget",
            module="main_widget",
            database="main_widget")

        return method(*args, **kwargs)

    def call(self, controller, method, **kwargs):
        """Call method on the cgteawork client.

        Args:
            controller: Client defined controller name.
            method (str, text_type): Client defined method name
                on the controller.
            **kwargs: Client defined method keyword arguments.

        Returns:
            dict or text_type: Recived data.
        """

        _kwargs = {
            'type': 'get'
        }
        _kwargs.update(kwargs)
        _kwargs['sign'] = controller
        _kwargs['method'] = method

        payload = json.dumps(_kwargs, indent=4, sort_keys=True)
        conn = create_connection(
            self.socket_url, core.CONFIG['CLIENT_TIMEOUT'])

        try:
            conn.send(payload)
            LOGGER.debug('SEND: %s', payload)
            recv = conn.recv()
            LOGGER.debug('RECV: %s', recv)
            ret = json.loads(recv)
            ret = ret['data']
            try:
                ret = json.loads(ret)
            except (TypeError, ValueError):
                pass
            return ret
        finally:
            conn.close()


def _get_typed_data(data, type_):
    assert isinstance(data, type_), type(data)
    return type_(data)


def _handle_error_10042(exception):
    if (isinstance(exception, OSError)
            and exception.errno == 10042):
        print("""
This is a bug of websocket-client 0.47.0 with python 3.6.4,
see: https://github.com/websocket-client/websocket-client/issues/404
""")
        raise exception
