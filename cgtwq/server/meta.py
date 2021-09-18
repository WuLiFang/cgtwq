# -*- coding=UTF-8 -*-
"""Server metadata."""

import cast_unknown as cast

from ..core import CONFIG
from ..model import StatusInfo
from . import http

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import List, Text, Tuple


def get_status(token=None):
    # type: (Text) -> Tuple[StatusInfo, ...]
    """Get all status on the server.

    Args:
        token (str): User token.

    Returns:
        tuple[StatusInfo]: Status data.
    """

    token = token or cast.text(CONFIG["DEFAULT_TOKEN"])
    resp = http.call("c_status", "get_all", token=token, field_array=StatusInfo._fields)
    return tuple(StatusInfo(*i) for i in resp)


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
