# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations
from typing import (
    Protocol,
)
from ._filter import Filter
from ._table_view_protocol import TableView
from ._pipeline_service_protocol import PipelineService
from ._flow_service_protocol import FlowService

class Client(Protocol):
    pipeline: PipelineService
    flow: FlowService
    def __init__(self, http_url: str = ...) -> None: ...
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
