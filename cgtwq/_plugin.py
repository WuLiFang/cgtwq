# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Text, Dict, Optional

import json

from ._util import iteritems, cast_text

from collections import OrderedDict
class Plugin:
    def __init__(self, id, name, type, raw_argv):
        # type: (Text, Text, Text, Text) -> None
        self.id = id
        self.name = name
        self.type = type
        self.raw_argv = raw_argv

    def argv(self):
        return PluginArguments(self.raw_argv)


def _try_parse_json(text):
    # type: (Text) -> Any
    try:
        return json.loads(text)
    except (TypeError, ValueError):
        return text


class PluginArguments:
    def __init__(self, raw):
        # type: (Text) -> None
        self._d = OrderedDict({})  # type: Dict[Text, PluginArgument]

        data = _try_parse_json(raw)
        if isinstance(data, dict):
            for k, v in iteritems(data):  # type: ignore
                if isinstance(v, dict):
                    self._d[k] = PluginArgument(  # type: ignore
                        cast_text(v.get("value", "")),  # type: ignore
                        cast_text(v.get("description", "")),  # type: ignore
                    )

    def encode(self):
        d = OrderedDict({})
        for k, v in iteritems(self._d):
            d[k] = dict(
                value=v.value,
                description=v.description,
            )
        return json.dumps(d)

    def __getitem__(self, key):
        # type: (Text) -> Text
        return self._d.get(key, PluginArgument()).value

    def __setitem__(self, key, value):
        # type: (Text, Text) -> ...
        self._d[key] = PluginArgument(value)

    def __iter__(self):
        for k, v in iteritems(self._d):
            yield k, v

    def __contains__(self, key):
        # type: (Text) -> ...
        return key in self._d

    def get(self, key, d=None):
        # type: (Text, Optional[PluginArgument]) -> ...
        return self._d.get(key, d)

    def add(self, key, description):
        # type: (Text, Text) -> None
        v = self.get(key)
        if not v :
            v = PluginArgument()
            self._d[key] = v
        v.description = description

class PluginArgument:
    def __init__(self, value="", description=""):
        # type: (Text,Text) -> None
        self.value = value
        self.description = description
