# -*- coding=UTF-8 -*-
"""Dummy desktop client for non win32 platform.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


class DesktopClient(object):
    """Dummy desktop client for non win32 platform.  """
    # pylint:disable=missing-docstring,no-self-use,unused-argument

    def __init__(self, socket_url=None):
        pass

    def connect(self):
        raise NotImplementedError

    @staticmethod
    def executable():
        return None

    def start(self):
        pass

    def is_running(self):
        return False

    def is_logged_in(self):
        return False

    def _refresh(self, database, module, is_selected_only):
        raise NotImplementedError

    def refresh(self, database, module):
        raise NotImplementedError

    def refresh_selected(self, database, module):
        raise NotImplementedError

    def token(self, max_age=2):
        raise NotImplementedError

    def _token(self):
        raise NotImplementedError

    def server_ip(self, max_age=5):
        raise NotImplementedError

    def _server_ip(self):
        raise NotImplementedError

    def server_http(self):
        raise NotImplementedError

    def selection(self):
        raise NotImplementedError

    def call(self, controller, method, **kwargs):
        raise NotImplementedError
