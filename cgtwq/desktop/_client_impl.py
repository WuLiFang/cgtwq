# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text
    from ._client import Client

import os
import sys

import psutil
from six.moves import configparser

from .._client_impl import ClientImpl as BaseClientImpl
from .._util import cast_text
from ._plugin_service_impl import new_plugin_service
from ._view_service_impl import new_view_service
from ._ws_client import WSClient

_WELL_KNOWN_EXE_PATH = [
    "C:/cgteamwork/bin/cgtw/CgTeamWork.exe",
    "C:/CgTeamWork_v7/bin/cgtw/CgTeamWork.exe",
    "C:/CgTeamWork_v6/bin/cgtw/CgTeamWork.exe",
]


def _default_exe_path():
    # type: () -> Text
    for i in (
        os.getenv("CGTEAMWORK_CLIENT_PATH", ""),
        # cgt6
        os.path.normpath(
            os.path.join(sys.executable, "..", "..", "bin", "cgtw", "CgTeamWork.exe")
        ),
        # cgt7
        os.path.normpath(
            os.path.join(
                sys.executable, "..", "..", "..", "bin", "cgtw", "CgTeamWork.exe"
            )
        ),
    ):
        if i and os.path.exists(i):
            return i

    for i in psutil.process_iter():  # type: ignore
        try:
            if i.name().lower() == "cgteamwork.exe":  # type: ignore
                return i.exe()  # type: ignore
        except psutil.AccessDenied:
            pass

    for i in _WELL_KNOWN_EXE_PATH:
        if i and os.path.exists(i):
            return i
    return ""


_FALLBACK_SOCKET_URL = os.getenv("CGTEAMWORK_DESKTOP_WEBSOCKET_URL", "")


class _ConfigFile:
    def __init__(self, exe_path):
        # type: (Text) -> None
        cfg_path = os.path.normpath(os.path.join(exe_path, "..", "config.ini"))
        self.cfg = configparser.ConfigParser()
        try:
            self.cfg.read(cfg_path)
        except Exception:
            pass

    def socket_url(self):
        port = self.cfg.get("General", "socket_server_port")
        if not port:
            return _FALLBACK_SOCKET_URL
        return "ws://127.0.0.1:%s" % port

    def http_url(self):
        host = self.cfg.get("General", "server")
        if not host:
            return ""
        https_port = self.cfg.get("General", "https_port")
        if not https_port:
            return "http://%s" % (host,)
        return "https://%s:%s" % (host, https_port)


class ClientImpl(BaseClientImpl):
    def __init__(self, exe_path="", socket_url=""):
        # type: (Text, Text) -> None
        self._exe_path = exe_path or _default_exe_path()
        cfg = _ConfigFile(self._exe_path)
        self._socket_url = socket_url or cfg.socket_url()
        self._ws = WSClient(self._socket_url)

        super(ClientImpl, self).__init__(
            http_url=cfg.http_url() or self._http_url_by_ws()
        )
        plugin = new_plugin_service(
            self._http,
            self._compat,
            self._ws,
        )
        view = new_view_service(
            self._ws,
            self._compat,
        )

        self.plugin = plugin
        self.view = view
        self.token = self._get_token()

    @property
    def exe_path(self):
        return self._exe_path

    @property
    def socket_url(self):
        return self._socket_url

    def _http_url_by_ws(self):
        host = self._ws.call_main_widget("get_server_ip")
        return "http://%s" % (host,)

    def _get_token(self):
        ret = self._ws.call_main_widget("get_token")
        if ret is True:
            return ""
        return cast_text(ret)


def new_client(exe_path="", socket_url=""):
    # type: (Text, Text) -> Client
    return ClientImpl(exe_path, socket_url)
