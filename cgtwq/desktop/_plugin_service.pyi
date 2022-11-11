# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations

from typing import Text, Protocol

from ._plugin_context_result import PluginContextResult
from .._plugin_service import PluginService as BasePluginService

class PluginService(BasePluginService, Protocol):
    def context(self, id: Text = ..., /) -> PluginContextResult:
        """context data for plugin

        Args:
            id: plugin id. Defaults to plugin launch argument
        """
    def report_result(self, ok: bool, /, *, id: Text = ...) -> None:
        """
        Tell client plugin execution result.
        if result is `False`, following operation will been aborted.
        """
