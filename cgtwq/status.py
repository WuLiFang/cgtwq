# -*- coding=UTF-8 -*-
"""Get status from server."""

from . import server

from .model import StatusInfo


def get_all():
    """Get all status.

    Returns:
        tuple[StatusInfo]: Status data.
    """

    token = server.setting.DEFAULT_TOKEN
    resp = server.call('c_status', 'get_all', token=token,
                       field_array=StatusInfo._fields)
    return tuple(StatusInfo(*i) for i in resp.data)
