# -*- coding=UTF-8 -*-
"""Common methods.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import time

from .filter import FilterList

CONFIG = {
    'SERVER_IP': '192.168.55.11',
    'DEFAULT_TOKEN': None,
    'DESKTOP_CLIENT_SOCKET_URL': 'ws://127.0.0.1:64999',
    'DESKTOP_CLIENT_HTTP_URL': 'ws://127.0.0.1:64998',  # NOT USED
    'CLIENT_TIMEOUT': 1,
}


class ControllerGetterMixin(object):
    """Mixin for controller getter.  """
    # pylint: disable=too-few-public-methods

    def _get_model(self, controller, method, model, filters):
        """Get infomation from controller with data model.

        Args:
            object (obj): Object to mixin.
            controller (str): Server defined controller name.
            method (str): Server defined method name.
            filters (FilterList): Filters.
            model (namedtuple): Data model.

        Returns:
            tuple[model]: Result
        """

        fields = getattr(model, 'fields', model._fields)
        resp = self.call(
            controller, method,
            field_array=fields,
            filter_array=FilterList(filters))
        return tuple(model(*i) for i in resp)


class CachedFunctionMixin(object):
    """Support function result cache.  """
    # pylint: disable=too-few-public-methods

    def __init__(self):
        super(CachedFunctionMixin, self).__init__()
        self.__cache = {}

    def _cached(self, key, func, max_age):
        now = time.time()
        if (key not in self.__cache
                or self.__cache[key][1] + max_age < now):
            self.__cache[key] = (func(), now)
        return self.__cache[key][0]
