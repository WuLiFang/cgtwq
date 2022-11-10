# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals


TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text
    from ._http_client import HTTPClient

from ._filter import Filter


class CompatService:
    LEVEL_UNKNOWN = 0
    LEVEL_5_2 = 1
    LEVEL_6_1 = 2

    @classmethod
    def level_from_version(cls, s):
        # type: (Text) -> int
        if not s:
            return cls.LEVEL_UNKNOWN

        if "5.0" <= s < "6.0":
            return cls.LEVEL_5_2
        if "6.0" <= s < "7.0":
            return cls.LEVEL_6_1
        return cls.LEVEL_UNKNOWN

    @classmethod
    def level_from_http(cls, http):
        # type: (HTTPClient) -> int

        resp = http.get("")
        return {"nginx/1.9.15": cls.LEVEL_5_2, "nginx/1.15.9": cls.LEVEL_6_1,}.get(
            resp.raw.headers.get("Server", ""),  # type: ignore
            cls.LEVEL_6_1,
        )

    def __init__(self, level):
        # type: (int) -> None
        self._l = level
        pass

    @property
    def level(self):
        return self._l

    def transform_field(self, s):
        # type: (Text) -> Text
        if self._l == self.LEVEL_5_2:
            return {
                "task.entity": "task.task_name",
                "shot.entity": "shot.shot",
                "eps.entity": "eps.eps_name",
                "shot.link_eps": "shot.eps_name",
                "asset.entity": "asset.asset_name",
                "project.entity": "project.code",
                "account.entity": "account.account",
                "asset_type.entity": "asset.type_name",
                "entity": "entity_name",
            }.get(s, s)
        return s

    def transform_filter(self, v):
        # type: (Filter) -> Filter

        ret = Filter(self.transform_field(v.left), v.op, v.right)
        if v.chain_to:
            ret = ret.chain(v.chain_logic, self.transform_filter(v.chain_to))
        return ret
