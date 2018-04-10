from . import server

from .model import StatusInfo


def get_all():
    token = server.setting.DEFAULT_TOKEN
    resp = server.call('c_status', 'get_all', token=token)
    return tuple(StatusInfo(*i) for i in resp.data)
