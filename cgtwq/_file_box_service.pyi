# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations

from typing import Protocol, Text, Iterator

from ._row_id import RowID
from ._file_box import FileBox

class FileBoxService(Protocol):
    def get_by_sign(
        self,
        id: RowID,
        sign: Text,
        /,
    ) -> FileBox: ...
    def all_submit(
        self,
        id: RowID,
        /,
    ) -> Iterator[FileBox]: ...
