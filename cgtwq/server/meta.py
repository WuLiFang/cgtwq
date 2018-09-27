# -*- coding=UTF-8 -*-
"""Server metadata."""

from . import http
from ..core import CONFIG
from ..model import StatusInfo


def get_status(token=None):
    """Get all status on the server.

    Args:
        token (str): User token.

    Returns:
        tuple[StatusInfo]: Status data.
    """

    token = token or CONFIG['DEFAULT_TOKEN']
    resp = http.call('c_status', 'get_all', token=token,
                     field_array=StatusInfo._fields)
    return tuple(StatusInfo(*i) for i in resp)


def get_software_types(token=None):
    """Get all software types on the server.

    Args:
        token ([type], optional): Defaults to None. [description]

    Returns:
        list[str]
    """

    token = token or CONFIG['DEFAULT_TOKEN']
    resp = http.call('c_status', 'get_software_type', token=token)
    return resp
