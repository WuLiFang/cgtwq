# -*- coding=UTF-8 -*-
"""Common methods.  """
from __future__ import absolute_import, division, print_function, unicode_literals

import time

from environs import Env

from deprecated import deprecated

from .filter import FilterList

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Text, Tuple, Callable


ENV = Env()
CONFIG = {
    "URL": ENV("CGTEAMWORK_URL", "http://192.168.55.11"),
    "API_VERSION": ENV("CGTEAMWORK_VERSION", ""),
    "DEFAULT_TOKEN": ENV("CGTEAMWORK_DEFAULT_TOKEN", ""),
    "DESKTOP_WEBSOCKET_URL": ENV(
        "CGTEAMWORK_DESKTOP_WEBSOCKET_URL", "ws://127.0.0.1:64999"
    ),
    "CONNECTION_TIMEOUT": ENV.int("CGTEAMWORK_CONNECTION_TIMEOUT", 1),
    "MIN_FETCH_INTERVAL": ENV.int("CGTEAMWORK_MIN_FETCH_INTERVAL", 1),
}
FIELD_TYPES = ("int", "decimal", "lineedit", "textedit", "checkbox", "list")


class ControllerGetterMixin(object):
    """Mixin for controller getter."""

    # pylint: disable=too-few-public-methods

    def _filter_model(self, controller, method, model, filters):
        # type: (Text, Text, Any, FilterList) -> Tuple[Any, ...]
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

        # TODO: move mixin to mixins/ folder
        from . import compat

        assert isinstance(filters, FilterList), type(filters)
        fields = getattr(model, "fields", model._fields)  # type: Any

        resp = self.call(  # type: ignore
            controller,
            method,
            field_array=[compat.adapt_field_sign(i) for i in fields],
            filter_array=compat.adapt_filters(filters),
        )
        return tuple(model(*i) for i in resp)

    filter_model = deprecated(
        version="3.0.0",
        reason="Renamed to _filter_model",
    )(_filter_model)


class CachedFunctionMixin(object):
    """Support function result cache."""

    # pylint: disable=too-few-public-methods

    def __init__(self):
        super(CachedFunctionMixin, self).__init__()
        self.__cache = {}

    def _cached(self, key, func, max_age):
        # type: (Text, Callable[[], Any], int) -> Any
        now = time.time()
        if key not in self.__cache or self.__cache[key][1] + max_age < now:
            self.__cache[key] = (func(), now)
        return self.__cache[key][0]
