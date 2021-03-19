# -*- coding=UTF-8 -*-
"""Handle CGTeamWork plugin metadata.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import time
from functools import partial

import cast_unknown as cast
import six

from . import core, server
from .filter import Field, FilterList
from .model import PluginArgumentInfo, PluginInfo

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Dict, List, Text, Union

    import cgtwq


def _accessor(field):
    # type: (Text) -> Any
    # pylint:disable=protected-access
    def _get(self): 
        # type: (Any) -> Any
        
        self.fetch()
        return getattr(self._cached_info, field)

    def _set(self, value):
        # type: (Any, Any) -> Any
        self.set_fields(**{
            _get_server_field(PluginInfo, field):
            value})

    return property(_get, _set)


@six.python_2_unicode_compatible
class PluginMeta(object):
    """ CGTeamWork plug-in metadata.  """

    name = _accessor('name')
    type = _accessor('type')

    def __init__(self, uuid):
        # type: (Text) -> None
        super(PluginMeta, self).__init__()
        self.uuid = uuid
        self.last_fetch_time = None
        self._cached_info = None

        self.call = partial(server.call, 'c_plugin', id=self.uuid)

        self.arguments = PluginMetaArguments(self, 'arguments')

    def __str__(self):
        return 'Plugin<uuid={0.uuid}, name={0.name}, type={0.type}>'.format(self)

    def fetch(self, token=None):
        # type: (Text) -> None
        """Fetch plugin data from server.  """

        if (self.last_fetch_time
                and (self.last_fetch_time - time.time() > core.CONFIG['MIN_FETCH_INTERVAL'])):  # type: ignore
            return

        token = token or cast.text(core.CONFIG['DEFAULT_TOKEN'])
        resp = server.call(
            'c_plugin', 'get_one_with_id',
            token=token,
            id=self.uuid,
            field_array=PluginInfo.fields,
        )
        self._cached_info = PluginInfo(*resp)

        self.last_fetch_time = time.time()

    def set_fields(self, token=None, **data):
        # type: (Text, *Any) -> None
        r"""Set field data for the plug-in.

        Args:
            token (str, optional): Defaults to None. User token.
            \*\*data: Field name as key, Value as value.
        """

        token = token or cast.text(core.CONFIG['DEFAULT_TOKEN'])

        self.call('set_one_with_id',
                  token=token,
                  id=self.uuid,
                  field_data_array=data)

        self.last_fetch_time = None

    def get_argument(self, key, token=None):
        # type: (Text, Text) -> PluginArgumentInfo
        """Get argument information.

        Args:
            key (str): Argument key.
            token (str, optional): Defaults to None. User token.

        Returns:
            PluginArgumentInfo: Plug-in argument information.
        """

        self.fetch(token=token)
        ret = self._cached_info.arguments[key]
        assert isinstance(ret, PluginArgumentInfo), type(ret)
        return ret

    def set_argument(self, key, value=None, description=None, token=None):
        # type: (Text, Text, Text, Text) -> None
        """Set argument data.

        Args:
            key (str): Data key.
            value (any, optional): Defaults to None. Data value.
            description (str, optional): Defaults to None. Argument description.
            token (str, optional): Defaults to None. User token.
        """

        payload = self.arguments.data

        default_value = None
        default_descrtion = ''

        if key in payload:
            old_value = payload[key]
            assert isinstance(old_value, PluginArgumentInfo), type(old_value)
            default_value = old_value.value
            default_descrtion = old_value.description

        new_value = PluginArgumentInfo(
            value=value if value is not None else default_value,
            description=description if description is not None else default_descrtion
        )

        payload[key] = new_value
        payload = {k: dict(v._asdict()) for k, v in payload.items()}

        for v in payload.values():
            v['value'] = json.dumps(v['value'])

        self.set_fields(
            token=token,
            argv=payload
        )

    @classmethod
    def filter(cls, filters=None, token=None):
        # type: (Union[cgtwq.Filter, cgtwq.FilterList], Text) -> List[PluginMeta]
        """Filter plugins from server.

        Args:
            filters (Filter or FilterList, optional): Defaults to None. Plugin filter
            token (str, optional): Defaults to None. User token.

        Returns:
            list[Plugin]: Matched plug-ins.
        """

        filters = filters or Field('#id').has('%')
        token = token or cast.text(core.CONFIG['DEFAULT_TOKEN'])

        filters = FilterList(filters)
        resp = server.call(
            'c_plugin', 'get_with_filter',
            token=token,
            field_array=PluginInfo.fields,
            filter_array=filters,
        )
        return [cls.from_info(PluginInfo(*i)) for i in resp]

    @classmethod
    def from_info(cls, info):
        # type: (PluginInfo) -> PluginMeta
        """Initialize Plugin object from info.

        Args:
            info (PluginInfo): Plugin information.

        Returns:
            Plugin
        """

        assert isinstance(info, PluginInfo), type(info)
        ret = cls(info.id)
        ret._cached_info = info  # pylint:disable=protected-access
        return ret


def _get_server_field(model, field):
    # type: (Any, Text) -> Text
    return model.fields[model._fields.index(field)]


class PluginMetaArguments(object):
    """Plugin metadata argument accessor.  """
    # pylint:disable=protected-access

    def __init__(self, plugin, field):
        # type: (PluginMeta, Text) -> None
        assert isinstance(plugin, PluginMeta), type(plugin)
        self.plugin = plugin
        self.field = field
        self.server_field = _get_server_field(PluginInfo, field)

    @property
    def data(self):
        # type: () -> Dict[Text, Any]
        """Corresponse information data.

        Returns:
            dict: A copy of data.
        """

        self.plugin.fetch()
        ret = getattr(self.plugin._cached_info, self.field)
        assert isinstance(ret, dict), type(ret)
        return dict(ret)

    def __getitem__(self, key):
        # type: (Text) -> Text
        return self.plugin.get_argument(key).value

    def __setitem__(self, key, value):
        # type: (Text, Any) -> None
        self.plugin.set_argument(key, value)

    def __delitem__(self, key):
        # type: (Text) -> None
        data = self.data
        del data[key]
        self.plugin.set_fields(**{self.server_field: data})
