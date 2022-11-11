# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Text, Dict
from collections import OrderedDict

import requests
import json
from . import exceptions

from ._util import PY2, cast_text, cast_binary


def _raise_error(result):
    # type: (Any) -> None
    if not isinstance(result, dict):
        return

    code, type_, data = (  # type: ignore
        result.get("code"),  # type: ignore
        result.get("type"),  # type: ignore
        result.get("data", result),  # type: ignore
    )

    if code is None:
        return
    elif code == "1":
        return
    elif (code, type_, data) == ("2", "msg", "please login!!!"):
        raise exceptions.LoginError
    msg = cast_text(data)
    if PY2:
        msg = cast_binary(msg)
    raise ValueError(msg)


class HTTPResponse:
    def __init__(self, raw):
        # type: (requests.Response) -> None
        self.raw = raw

    def json(self):
        # type: () -> Any
        data = self.raw.json()  # type: ignore
        _raise_error(data)
        if not isinstance(data, dict):
            return data
        return data.get("data", data)  # type: ignore


class JSONEncoder(json.JSONEncoder):
    def default(
        self,
        o,
    ):
        # type: (Any, Any) -> Any
        method = getattr(o, "as_payload", None)
        if callable(method):
            return method()
        if isinstance(o, set):
            return list(o) # type: ignore
        if isinstance(o, OrderedDict):
            return dict(o) # type: ignore
        return super(JSONEncoder, self).default(o)  # type: ignore


class HTTPClient:
    def __init__(self, url):
        # type: (Text) -> None
        self._url = url
        self._session = requests.Session()
        self.token = ""
        self._encoder = JSONEncoder()

    def __del__(self):
        self._session.close()

    def _build_url(self, pathname):
        # type: (Text) -> Text
        return "{}/{}".format(self._url, pathname.lstrip("\\/"))

    @property
    def url(self):
        return self._url

    def post(self, pathname, data, **kwargs):
        # type: (Text, Dict[Text, Any],  *Any) -> HTTPResponse

        assert "data" not in kwargs
        if data is not None:
            data = {
                "data": self._encoder.encode(data),
            }
        return HTTPResponse(
            self._session.post(  # type: ignore
                self._build_url(pathname),
                data=data,
                cookies={"token": self.token},
                **kwargs
            )
        )

    def get(self, pathname, **kwargs):
        # type: (Text,  *Any) -> HTTPResponse

        return HTTPResponse(
            self._session.get(self._build_url(pathname), cookies={"token": self.token}, **kwargs)  # type: ignore
        )

    def call(self, controller, method, **data):
        # type: (Text, Text, *Any) -> HTTPResponse
        """Call controller method ."""

        data["controller"] = controller
        data["method"] = method

        return self.post("api.php", data)
