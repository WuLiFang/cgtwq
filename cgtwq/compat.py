# -*- coding=UTF-8 -*-
# pyright: strict
"""Compatible layer for different api version.  """

from __future__ import absolute_import, division, print_function, unicode_literals

import six

from . import core, filter

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Dict, Sequence, Text, Union

API_LEVEL_5_2 = 0
API_LEVEL_6_1 = 1


_API_LEVEL_CACHE = {}  # type: Dict[Text, int]


def api_level():
    # type: () -> int

    versionText = core.CONFIG["API_VERSION"]
    if "5.0" <= versionText < "6.0":
        return API_LEVEL_5_2
    if "6.0" <= versionText:
        return API_LEVEL_6_1

    _cache_key = core.CONFIG["URL"]
    if _cache_key not in _API_LEVEL_CACHE:
        from . import server

        resp = server.http.SESSION.get(core.CONFIG["URL"])
        _API_LEVEL_CACHE[_cache_key] = {
            "nginx/1.9.15": API_LEVEL_5_2,
            "nginx/1.15.9": API_LEVEL_6_1,
        }.get(
            resp.headers.get("Server", ""),
            API_LEVEL_6_1,
        )
    return _API_LEVEL_CACHE[_cache_key]


def adapt_field_sign(s):
    # type: (Text) -> Text
    if api_level() == API_LEVEL_5_2:
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


def adapt_filter(f):
    # type: (Sequence[Text]) -> filter.Filter
    left, operator, right = f
    return filter.Filter(adapt_field_sign(left), right, operator)


def adapt_filters(filter_list):
    # type: (Sequence[Union[Text, Sequence[Text]]]) -> filter.FilterList

    ret = []  # type: Sequence[Union[Text,Sequence[Text]]]
    for i in filter_list:
        if isinstance(i, (str, six.text_type)):
            ret.append(i)
        else:
            ret.append(adapt_filter(i))

    return filter.FilterList(ret)
