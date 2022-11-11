# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations
from typing import (
    Protocol,
)
from ._filter import Filter
from ._table_view import TableView
from ._pipeline_service import PipelineService
from ._flow_service import FlowService

class Client(Protocol):
    pipeline: PipelineService
    flow: FlowService
    def __init__(self, http_url: str = ..., version: str = ...) -> None: ...
    @property
    def http_url(self) -> str: ...
    @property
    def token(self) -> str: ...
    @token.setter
    def token(self, v: str) -> None: ...
    def table(
        self,
        database: str,
        module: str,
        module_type: str,
        /,
        *,
        filter_by: Filter = ...,
    ) -> TableView: ...
