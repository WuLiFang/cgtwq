# -*- coding=UTF-8 -*-
"""Get information from CGTeamWork GUI client.  """

from __future__ import absolute_import, print_function, unicode_literals

import logging
import os
from functools import partial
from subprocess import Popen

import psutil
import websocket as ws
from deprecated import deprecated
from six import text_type

from ...core import CONFIG, CachedFunctionMixin
from ...exceptions import IDError
from ...selection import Selection
from . import core
from .plugin import DesktopClientPlugin
import configparser

LOGGER = logging.getLogger(__name__)

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Text, Type, TypeVar

    T = TypeVar("T")


def _default_socket_url():
    cfg_path = DesktopClient.config_path()
    if cfg_path:
        try:
            cfg = configparser.ConfigParser()
            cfg.read(cfg_path)
            port = cfg.get("General", "socket_server_port")
            LOGGER.debug("ws port: %s", port)
            return "ws://127.0.0.1:%s" % port
        except Exception as ex:
            LOGGER.warn("read config failed: %s", ex)
    return CONFIG["DESKTOP_WEBSOCKET_URL"]


class DesktopClient(CachedFunctionMixin):
    """Communicate with a CGTeamWork official GUI clients."""

    def __init__(self, socket_url=None):
        # type: (str) -> None
        super(DesktopClient, self).__init__()
        self.socket_url = socket_url or _default_socket_url()

        # Attachment.
        self.plugin = DesktopClientPlugin(self)

        # Shorthand method.
        self.call_main_widget = partial(
            self.call, "main_widget", module="main_widget", database="main_widget"
        )

    def connect(self):
        """Update module config from desktop client."""

        CONFIG["URL"] = "http://{}".format(self.server_ip())
        CONFIG["DEFAULT_TOKEN"] = self.token()

    @staticmethod
    def executable():
        """Get a cgteamwork client executable.

        Returns:
            text_type: Executable path.
        """

        # Get client executable.
        for i in psutil.process_iter():
            try:
                if i.name().lower() == "cgteamwork.exe":
                    return i.exe()
            except psutil.AccessDenied:
                pass

        # Try use default path when client not running.
        for i in (
            os.getenv("CGTEAMWORK_CLIENT_PATH", ""),
            "C:/CgTeamWork_v6/bin/cgtw/CgTeamWork.exe",
            "C:/cgteamwork/bin/cgtw/CgTeamWork.exe",
        ):
            if i and os.path.exists(i):
                return i
        return None

    @staticmethod
    def config_path():
        exe_path = DesktopClient.executable()
        if not exe_path:
            return
        return os.path.join(os.path.dirname(exe_path), "config.ini")

    def start(self):
        """Start client if not running."""

        executable = self.executable()
        if executable and not self.is_running():
            Popen(executable, cwd=os.path.dirname(executable), close_fds=True)

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
        # type: (Text, Text, bool) -> None
        self.call(
            "view_control",
            "refresh_select" if is_selected_only else "refresh",
            module=module,
            database=database,
            type="send",
        )

    def refresh(self, database, module):
        # type: (Text, Text) -> None
        """
        Refresh specified view in client
        if matched view is opened.

        Args:
            database (text_type): Database of view.
            module (text_type): Module of view.
        """

        self._refresh(database, module, False)

    def refresh_selected(self, database, module):
        # type: (Text, Text) -> None
        """
        Refresh selected part of specified view in client
        if matched view is opened.

        Args:
            database (text_type): Database of view.
            module (text_type): Module of view.
        """

        self._refresh(database, module, True)

    def token(self, max_age=2):
        # type: (int) -> None
        """Cached client token."""

        return self._cached("token", self._token, max_age)

    def _token(self):
        """Client token."""

        ret = self.call_main_widget("get_token")
        if ret is True:
            return ""
        assert isinstance(ret, text_type), type(ret)
        return text_type(ret)

    def server_ip(self, max_age=5):
        # type: (int) -> None
        """Cached server ip."""

        return self._cached("server_ip", self._server_ip, max_age)

    def _server_ip(self):
        """Server ip current using by client."""

        ret = self.call_main_widget("get_server_ip")
        if ret is True:
            return ""
        return _get_typed_data(
            ret,
            text_type,
        )

    def server_http(self):
        """Server http current using by client."""

        ret = self.call_main_widget("get_server_http")
        if ret is True:
            ret = ""
        return _get_typed_data(
            ret,
            text_type,
        )

    def selection(self):
        """Get current selection from client.

        Returns:
            Selection: Current selection.
        """

        try:
            plugin_data = self.get_plugin_data()
        except IDError:
            # TODO: should raise exception.EmptySelection.
            raise ValueError("Empty selection.")
        return Selection.from_data(**plugin_data._asdict())

    def call(self, controller, method, **kwargs):
        # type: (Text, Text, *Any) -> Any
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
        version="3.0.0",
        reason="Use `Desktop.selection` instead.",
    )(selection)

    get_plugin_data = deprecated(
        version="3.0.0",
        reason="Use `DesktopClient.plugin.data` instead.",
    )(lambda self, uuid="": self.plugin.data(uuid))

    send_plugin_result = deprecated(
        version="3.0.0", reason="Use `DesktopClient.plugin.send_result` instead."
    )(
        lambda self, uuid, result=False: self.plugin.send_result(
            process_id=uuid, result=result
        )
    )


def _get_typed_data(data, type_):
    # type: (Any, Type[T]) -> T
    assert isinstance(data, type_), type(data)
    return type_(data)  # type: ignore
