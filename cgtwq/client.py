# -*- coding=UTF-8 -*-
"""Get information from CGTeamWork GUI client.  """

from __future__ import absolute_import, print_function, unicode_literals

import json
import logging
import os
import socket
import time
from collections import namedtuple
from functools import partial
from subprocess import Popen

from six import text_type
from websocket import create_connection

from wlf.decorators import deprecated

from .server import setting
from .exceptions import IDError

CGTeamWorkClientStatus = namedtuple(
    'CGTeamWorkClientStatus',
    ('server_ip', 'server_http', 'token'))
PluginData = namedtuple(
    'PulginData',
    ('plugin_id',
     'filebox_id',
     'database',
     'module',
     'id_list',
     'folder',
     'file_path_list',
     'argv')
)
LOGGER = logging.getLogger(__name__)


class CGTeamWorkClient(object):
    """Query from CGTeamWork GUI clients.  """

    url = "ws://127.0.0.1:64999"
    qt_url = 'ws://127.0.0.1:64998'
    time_out = 1
    cache = {}

    def __init__(self):
        self.start()
        self.status = CGTeamWorkClientStatus(
            server_ip=self.server_ip(),
            server_http=self.server_http(),
            token=self.token(),
        )

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

    @classmethod
    def start(cls):
        """Start client if not running.  """

        executable = cls.executable()
        if executable and not cls.is_running():
            Popen(executable,
                  cwd=os.path.dirname(executable),
                  close_fds=True)

    @classmethod
    def is_running(cls):
        """Check if client is running.

        Returns:
            bool: Ture if client is running.
        """

        try:
            cls.token(-1)
            return True
        except (socket.error, socket.timeout):
            pass

        return False

    @classmethod
    def is_logged_in(cls):
        """Check if client is logged in.

        Returns:
            bool: True if client is logged in.
        """

        try:
            if cls.token(-1):
                return True
        except (socket.error, socket.timeout):
            pass

        return False

    @classmethod
    def refresh(cls, database, module):
        """
        Refresh specified view in client
        if matched view is opened.

        Args:
            database (text_type): Database of view.
            module (text_type): Module of view.
        """

        cls.call('view_control', 'refresh',
                 module=module,
                 database=database,
                 type='send')

    @classmethod
    def refresh_select(cls, database, module):
        """
        Refresh selected part of specified view in client
        if matched view is opened.

        Args:
            database (text_type): Database of view.
            module (text_type): Module of view.
        """

        cls.call(
            'view_control', 'refresh_select',
            module=module,
            database=database,
            type='send',
        )

    @classmethod
    def _cached(cls, key, func, max_age):
        now = time.time()
        if (key not in cls.cache
                or cls.cache[key][1] + max_age < now):
            cls.cache[key] = (func(), now)
        return cls.cache[key][0]

    @classmethod
    def token(cls, max_age=2):
        """Cached client token.  """

        return cls._cached('token', cls._token, max_age)

    @classmethod
    def _token(cls):
        """Client token.  """

        ret = cls.call_main_widget("get_token")
        if ret is True:
            return ''
        assert isinstance(ret, text_type), type(ret)
        return text_type(ret)

    @classmethod
    def server_ip(cls, max_age=5):
        """Cached server ip.  """

        return cls._cached('server_ip', cls._server_ip, max_age)

    @classmethod
    def _server_ip(cls):
        """Server ip current using by client.  """

        ret = cls.call_main_widget("get_server_ip")
        assert isinstance(ret, text_type), type(ret)
        return text_type(ret)

    @classmethod
    def server_http(cls):
        """Server http current using by client.  """

        ret = cls.call_main_widget("get_server_http")
        assert isinstance(ret, text_type), type(ret)
        return text_type(ret)

    @classmethod
    def get_plugin_data(cls, uuid=''):
        """Get plugin data for uuid.

        Args:
            uuid (text_type): Plugin uuid.
        """

        data = cls.call_main_widget("get_plugin_data", plugin_uuid=uuid)
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

    @classmethod
    def send_plugin_result(cls, uuid, result=False):
        """
        Tell client plugin execution result.
        if result is `False`, following operation will been abort.

        Args:
            uuid (text_type): Plugin uuid.
            result (bool, optional): Defaults to False. Plugin execution result.
        """

        cls.call_main_widget("exec_plugin_result",
                             uuid=uuid,
                             result=result,
                             type='send')

    @classmethod
    def call_main_widget(cls, *args, **kwargs):
        """Send data to main widget.

        Args:
            **data (dict): Data to send.

        Returns:
            dict or text_type: Recived data.
        """

        method = partial(
            cls.call, "main_widget",
            module="main_widget",
            database="main_widget")

        return method(*args, **kwargs)

    @classmethod
    def call(cls, controller, method, **kwargs):
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
        _kwargs['class_name'] = controller
        _kwargs['method_name'] = method

        payload = json.dumps(_kwargs, indent=4, sort_keys=True)
        conn = create_connection(cls.url, cls.time_out)

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

    @classmethod
    @deprecated('Use `call_main_widget` instead.')
    def send_main_widget(cls, *args, **kwargs):
        """Depreacted. Use `call_main_widget` instead.  """

        return cls.call_main_widget(*args, **kwargs)

    @classmethod
    @deprecated('Use `call` instead.')
    def send(cls, *args, **kwargs):
        """Depreacted. Use `call` instead.  """

        return cls.call(*args, **kwargs)


def update_setting():
    """Update setting from desktop client.   """

    setting.SERVER_IP = CGTeamWorkClient.server_ip()
    setting.DEFAULT_TOKEN = CGTeamWorkClient.token()
