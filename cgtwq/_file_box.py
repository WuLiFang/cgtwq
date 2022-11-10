# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Text

from ._util import cast_text, parse_yes_no


class FileBox:
    def __init__(self, raw):
        # type: (dict[Text, Any]) -> None
        self.raw = raw

    def get_text(self, key, d=""):
        # type: (Text, Text) -> Text
        return cast_text(self.raw.get(key, d))

    def get_bool(self, key):
        # type: (Text) -> bool
        return parse_yes_no(self.get_text(key))

    @property
    def id(self):
        return self.get_text("#id")

    @property
    def path(self):
        return self.get_text("path")

    @property
    def classify(self):
        return self.get_text("classify")

    @property
    def title(self):
        return self.get_text("title")

    @property
    def sign(self):
        return self.get_text("sign")

    @property
    def color(self):
        return self.get_text("color")

    @property
    def server_id(self):
        return self.get_text("server_id")

    # @property
    # def rule(self):
    #     return self.raw.get("rule")

    # @property
    # def rule_view(self):
    #     return self.raw.get("rule_view")

    # @property
    # def server(self):
    #     return self.raw.get("server")

    # @property
    # def rule_view(self):
    #     return self.raw.get("drag_in")

    @property
    def is_submit(self):
        return self.get_bool("is_submit")

    @property
    def is_move_old_to_history(self):
        return self.get_bool("is_move_old_to_history")

    @property
    def is_move_same_to_history(self):
        return self.get_bool("is_move_same_to_history")

    @property
    def is_in_history_add_version(self):
        return self.get_bool("is_in_history_add_version")

    @property
    def is_in_history_add_datetime(self):
        return self.get_bool("is_in_history_add_datetime")

    @property
    def is_cover_disable(self):
        return self.get_bool("is_cover_disable")

    @property
    def is_msg_to_first_qc(self):
        return self.get_bool("is_msg_to_first_qc")
