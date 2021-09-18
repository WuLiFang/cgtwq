# -*- coding=UTF-8 -*-
"""Create http connection with cgtw server.  """
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import logging
from collections import OrderedDict

import requests
import cast_unknown as cast

from .. import core, exceptions

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Text, Dict


LOGGER = logging.getLogger(__name__)
SESSION = requests.Session()


def _json_default(self, obj):
    # type: (Any, Any) -> Any
    if isinstance(obj, OrderedDict):
        return dict(obj)
    _asdict = getattr(obj, "_asdict", None)
    if callable(_asdict):
        return _asdict()
    return json.JSONEncoder.default(self, obj)


def _raise_error(result):
    # type: (Any) -> None
    if not isinstance(result, dict):
        return

    code, type_, data = (
        result.get("code"),
        result.get("type"),
        result.get("data", result),
    )

    if code is None:
        return
    elif code == "1":
        return
    elif (code, type_, data) == ("2", "msg", "please login!!!"):
        raise exceptions.LoginError
    raise ValueError(cast.binary(data))


def _cgteamwork_url(pathname):
    # type: (Text) -> Text
    return "{}/{}".format(core.CONFIG["URL"], pathname.lstrip("\\/"))


def call(controller, method, token, **data):
    # type: (Text, Text, Text, *Any) -> Any
    """Call method on server controller.

    Args:
        controller (str): Controller name.
        method (str): Method name.
        token (str): User token.

    Returns:
        Method result.
    """

    data["controller"] = controller
    data["method"] = method

    return post("api.php", data, token)


def post(pathname, data, token, **kwargs):
    # type: (Text, Dict[Text, Any], Text, *Any) -> Any
    r"""`POST` data to CGTeamWork server.

    Args:
        pathname (str): Pathname for http host.
        data: Data to post.
        token (str): User token.
        \*\*kwargs: kwargs for `requests.post`

    Returns:
        Server execution result.
    """
    # pylint: disable=invalid-name

    assert "cookies" not in kwargs
    assert "data" not in kwargs

    LOGGER.debug("POST: %s: %s", pathname, data)
    if data is not None:
        data = {"data": json.JSONEncoder(default=_json_default).encode(data)}
    resp = SESSION.post(
        _cgteamwork_url(pathname), data=data, cookies={"token": token}, **kwargs
    )
    LOGGER.debug("RECV: %s", resp.text.strip())
    json_ = resp.json()
    _raise_error(json_)
    if not isinstance(json_, dict):
        return json_
    return json_.get("data", json_)


def get(pathname, token, **kwargs):
    # type: (Text, Text, *Any) -> Any
    r"""`GET` request to CGTeamWork server.

    Args:
        token (str unicode, optional): Defaults to None. If `token` is None,
            will use token from setting.
        \*\*kwargs: kwargs for `requests.get`

    Returns:
        json server response .
    """
    # pylint: disable=invalid-name

    assert "cookies" not in kwargs

    LOGGER.debug("GET: kwargs: %s", kwargs)
    resp = SESSION.get(_cgteamwork_url(pathname), cookies={"token": token}, **kwargs)
    LOGGER.debug("GET: %s", resp.text.strip())
    json_ = resp.json()
    _raise_error(json_)
    if not isinstance(json_, dict):
        return json_
    return json_.get("data", json_)
