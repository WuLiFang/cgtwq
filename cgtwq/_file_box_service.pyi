# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations

from typing import Protocol, Text

from ._row_id import RowID
from ._file_box import FileBox

class FileBoxService(Protocol):
    def get_by_sign(
        self,
        row: RowID,
        sign: Text,
        /,
    ) -> FileBox: ...
