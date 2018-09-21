# -*- coding=UTF-8 -*-
"""Client attachment for plugin related features.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
from uuid import UUID

import six

from . import core
from ...exceptions import IDError
from ...model import PluginData


def _is_plugin_uuid(text):
    text = six.text_type(text)
    try:
        return text == six.text_type(UUID(text))
    except (TypeError, ValueError):
        return False


class DesktopClientPlugin(core.DesktopClientAttachment):
    """Desktop client plugin operations."""

    @staticmethod
    def uuid():
        """UUID for current plugin.

        Returns:
            str: UUID,
                will be empty string when
                python has not been started
                from desktop client.
        """

        ret = '' if len(sys.argv) < 2 else sys.argv[-1]
        if not _is_plugin_uuid(ret):
            ret = ''
        return ret

    def data(self, uuid=None):
        """Get plugin data for uuid.

        Args:
            uuid (str, optional): Defaults to None, Plugin uuid.

        Returns:
            PluginData: Plugin data.
        """

        uuid = uuid or self.uuid()
        client = self.client
        data = client.call_main_widget(
            "get_plugin_data",
            plugin_uuid=uuid)
        if not data:
            msg = 'No matched plugin'
            if uuid:
                msg += ': {}'.format(uuid)
            msg += '.'
            raise IDError(msg)
        assert isinstance(data, dict), type(data)
        for i in PluginData._fields:
            data.setdefault(i, None)
        return PluginData(**data)

    def send_result(self, result, uuid=None):
        """
        Tell client plugin execution result.
        if result is `False`, following operation will been abort.

        Args:
            result (bool): Plugin execution result.
            uuid (str, optional): Defaults to None, Plugin uuid.
        """

        uuid = uuid or self.uuid()
        client = self.client
        client.call_main_widget("exec_plugin_result",
                                uuid=uuid,
                                result=result,
                                type='send')
