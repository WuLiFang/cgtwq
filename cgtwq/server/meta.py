# -*- coding=UTF-8 -*-
"""Server metadata."""

import cast_unknown as cast

from ..core import CONFIG
from ..model import StatusInfo
from . import http
from .. import compat

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import List, Text, Tuple, Optional


def _get_status_v5_2(token):
    # type: (Text) -> Tuple[StatusInfo, ...]
    token = token or cast.text(CONFIG["DEFAULT_TOKEN"])
    resp = http.call("c_status", "get_all", token=token, field_array=StatusInfo._fields)
    return tuple(StatusInfo(*i) for i in resp)


def _get_status_v6_1(token):
    # type: (Text) -> Tuple[StatusInfo, ...]
    resp = http.call(
        "c_status", "get_status_and_color", token=token, field_array=StatusInfo._fields
    )
    return tuple(
        StatusInfo(status=status, color=color) for status, color in dict(resp).items()
    )


def get_status(token=None):
    # type: (Optional[Text]) -> Tuple[StatusInfo, ...]
    """Get all status on the server.

    Args:
        token (str): User token.

    Returns:
        tuple[StatusInfo]: Status data.
    """
    token = token or cast.text(CONFIG["DEFAULT_TOKEN"])
    if compat.api_level() == compat.API_LEVEL_5_2:
        return _get_status_v5_2(token)
    return _get_status_v6_1(token)


def get_software_types(token=None):
    # type: (Text) -> List[Text]
    """Get all software types on the server.

    Args:
        token ([type], optional): Defaults to None. [description]

    Returns:
        list[str]
    """

    token = token or cast.text(CONFIG["DEFAULT_TOKEN"])
    resp = http.call("c_status", "get_software_type", token=token)
    return resp
