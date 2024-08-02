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
from ._user_token import UserToken
from ._file_box_service import FileBoxService
from ._image_service import ImageService

class Client(Protocol):
    pipeline: PipelineService
    flow: FlowService
    file_box: FileBoxService
    image: ImageService

    def __init__(self, http_url: str = ..., version: str = ...) -> None: ...
    @property
    def http_url(self) -> str: ...
    @property
    def token(self) -> UserToken: ...
    @token.setter
    def token(self, v: UserToken) -> None: ...
    def table(
        self,
        database: str,
        module: str,
        module_type: str,
        /,
        *,
        filter_by: Filter = ...,
    ) -> TableView: ...
