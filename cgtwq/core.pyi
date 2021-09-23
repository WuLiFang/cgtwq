from cgtwq.filter import FilterList
from typing import Any, Callable, Text, Tuple, TypedDict

class _Config(TypedDict):
    URL: Text
    API_VERSION: Text
    DEFAULT_TOKEN: Text
    DESKTOP_WEBSOCKET_URL: Text
    CONNECTION_TIMEOUT: int
    MIN_FETCH_INTERVAL: int

CONFIG: _Config

FIELD_TYPES: Tuple[Text, ...]

class ControllerGetterMixin:
    def _filter_model(
        self, controller: Text, method: Text, model: Any, filters: FilterList
    ) -> Tuple[Any, ...]: ...

class CachedFunctionMixin:
    def _cached(self, key: Text, func: Callable[[], Any], max_age: int) -> Any: ...
