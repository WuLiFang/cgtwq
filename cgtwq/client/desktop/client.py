# -*- coding=UTF-8 -*-
"""Get information from CGTeamWork GUI client.  """

from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
import logging
import os
from subprocess import Popen

from six import text_type
import websocket as ws
from wlf.decorators import deprecated

from . import core
from ...core import CONFIG, CachedFunctionMixin
from ...exceptions import IDError
from ...selection import Selection
from .plugin import DesktopClientPlugin

LOGGER = logging.getLogger(__name__)


class DesktopClient(CachedFunctionMixin):
    """Communicate with a CGTeamWork official GUI clients.  """

    def __init__(self, socket_url=None):
        super(DesktopClient, self).__init__()
        self.socket_url = socket_url or CONFIG['DESKTOP_WEBSOCKET_URL']

        # Attachment.
        self.plugin = DesktopClientPlugin(self)

        # Shorthand method.
        self.call_main_widget = partial(
            self.call, "main_widget",
            module="main_widget",
            database="main_widget")

    def connect(self):
        """Update module config from desktop client.  """

        CONFIG['URL'] = 'http://{}'.format(self.server_ip())
        CONFIG['DEFAULT_TOKEN'] = self.token()

    @staticmethod
    def executable():
        """Get a cgteamwork client executable.

        Returns:
            text_type: Executable path.
        """

        # Get client executable.
        try:
            executable = os.path.abspath(os.path.join(
                __import__('cgtw').__file__, '../../cgtw/CgTeamWork.exe'))
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
            bool: True if client is running.
        """

        try:
            self.token(-1)
            return True
        except (IOError, ws.WebSocketException):
            pass
        return False

    def is_logged_in(self):
        """Check if client is logged in.

        Returns:
            bool: True if client is logged in.
        """

        try:
            if self.token(-1):
                return True
        except (IOError, ws.WebSocketException):
            pass
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

        return _get_typed_data(
            self.call_main_widget("get_server_ip"),
            text_type)

    def server_http(self):
        """Server http current using by client.  """

        return _get_typed_data(
            self.call_main_widget("get_server_http"),
            text_type)

    def selection(self):
        """Get current selection from client.

        Returns:
            Selection: Current selection.
        """

        try:
            plugin_data = self.get_plugin_data()
        except IDError:
            # TODO: should raise exception.EmptySelection.
            raise ValueError('Empty selection.')
        return Selection.from_data(**plugin_data._asdict())

    def call(self, controller, method, **kwargs):
        r"""Call method on the cgteamwork client.

        Args:
            controller (str): Client defined controller name.
            method (str): Client defined method name on the controller.
            \*\*kwargs: Client defined method keyword arguments.

        Returns:
            dict or str: Received data.
        """

        return core.call(self.socket_url, controller, method, **kwargs)

    # Deprecated methods.

    current_select = deprecated(
        selection, reason='Use `Desktop.selection` instead.')

    get_plugin_data = deprecated(
        lambda self, uuid='': self.plugin.data(uuid),
        reason='Use `DesktopClient.plugin.data` instead.')

    send_plugin_result = deprecated(
        (lambda self, uuid, result=False:
         self.plugin.send_result(process_id=uuid, result=result)),
        reason='Use `DesktopClient.plugin.send_result` instead.'
    )


def _get_typed_data(data, type_):
    assert isinstance(data, type_), type(data)
    return type_(data)
