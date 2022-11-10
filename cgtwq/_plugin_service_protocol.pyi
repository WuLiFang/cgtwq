# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations
from typing import (
    Protocol,
    Iterator,
    Iterable,
)
from ._filter import Filter
from ._table_view_protocol import TableView
from ._plugin import Plugin

class PluginService(Protocol):
    def table(
        self,
        /,
        *,
        filter_by: Filter = ...,
    ) -> TableView: ...
    def find(
        self,
        /,
        *,
        filter_by: Filter = ...,
    ) -> Iterator[Plugin]: ...
    def get(
        self,
        id: str,
        /,
    ) -> Plugin: ...
    def save(
        self,
        obj: Plugin,
        /,
        *,
        only_fields: Iterable[str] = ...,
    ) -> None: ...
