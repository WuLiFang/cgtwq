# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Text, Dict, List

from .._field_sign import FieldSign
from .._row_id import RowID
from .._util import cast_list, cast_text


class PluginContextResult:
    def __init__(self, raw):
        # type: (Dict[Text, Any]) -> None
        self.raw = raw

    def get_text(self, key, d=""):
        # type: (Text, Text) -> Text
        return cast_text(self.raw.get(key, d))

    def get_text_list(self, key):
        # type: (Text) -> List[Text]
        return [cast_text(i) for i in cast_list(self.raw.get(key, []))]

    @property
    def plugin_id(self):
        return self.get_text("plugin_id")

    @property
    def file_box_id(self):
        # spell-checker: word filebox_id
        return self.get_text("filebox_id")

    @property
    def database(self):
        return self.get_text("database")

    @property
    def module(self):
        return self.get_text("module")

    @property
    def module_type(self):
        return self.get_text("module_type")

    @property
    def id_list(self):
        return self.get_text_list("id_list")

    @property
    def folder(self):
        return self.get_text("folder")

    @property
    def file_paths(self):
        return self.get_text_list("file_path_list")

    @property
    def argv(self):
        # type: () -> Dict[Text, Text]
        return self.raw.get("argv", {})

    @property
    def retake_pipeline_ids(self):
        return self.get_text_list("retake_pipeline_id_list")

    @property
    def link_ids(self):
        return self.get_text_list("link_id_list")

    @property
    def qc_field_sign(self):
        return FieldSign(self.get_text("qc_field_sign"))

    def row_ids(self):
        db = self.database
        module = self.module
        module_type = self.module_type
        return [RowID(db, module, module_type, i) for i in self.id_list]
