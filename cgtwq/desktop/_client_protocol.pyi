# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations

from typing import Protocol

from .._client_protocol import Client as BaseClient
from ._plugin_service_protocol import PluginService
from ._view_service_protocol import ViewService

class Client(BaseClient, Protocol):
    plugin: PluginService
    view: ViewService
    def __init__(self, *, exe_path: str = ..., socket_url: str = ...) -> None: ...
    @property
    def exe_path(self) -> str: ...
    @property
    def socket_url(self) -> str: ...
