# -*- coding=UTF-8 -*-
"""Client attachment for plugin related features.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
from uuid import UUID

import six

from wlf.decorators import deprecated

from . import core
from ...exceptions import IDError
from ...model import PluginData
from ...plugin_meta import PluginMeta


def _is_uuid(text):
    text = six.text_type(text)
    try:
        return text.lower() == six.text_type(UUID(text))
    except (TypeError, ValueError):
        return False


class DesktopClientPlugin(core.DesktopClientAttachment):
    """Desktop client plugin operations."""

    @staticmethod
    def process_id():
        """Current plugin process id.

        Returns:
            str: Process id,
                will be empty string when
                python has not been started
                from desktop client.
                Empty string indicate
                last launched plugin process.
        """

        if sys.argv and _is_uuid(sys.argv[-1]):
            return sys.argv[-1]
        return ''

    def data(self, process_id=None):
        """Get plugin data with process_id.

        Args:
            process_id (str, optional): Defaults to None, Plugin process uuid.

        Returns:
            PluginData: Plugin data.
        """

        process_id = process_id or self.process_id()
        client = self.client
        data = client.call_main_widget(
            "get_plugin_data",
            plugin_uuid=process_id)
        if not data:
            msg = 'No matched plugin process'
            if process_id:
                msg += ': {}'.format(process_id)
            msg += '.'
            raise IDError(msg)
        if data is True:
            data = {}
        assert isinstance(data, dict), type(data)
        for i in PluginData._fields:
            if i in ("id_list", "file_path_list", "retake_pipeline_id_list"):
                data.setdefault(i, [])
            else:
                data.setdefault(i, None)
        return PluginData(**data)

    def send_result(self, result, process_id=None):
        """
        Tell client plugin execution result.
        if result is `False`, following operation will been abort.

        Args:
            result (bool): Plugin execution result.
            process_id (str, optional): Defaults to None, Plugin process uuid.
        """

        process_id = process_id or self.process_id()
        client = self.client
        client.call_main_widget("exec_plugin_result",
                                uuid=process_id,
                                result=result,
                                type='send')

    def metadata(self):
        """Get plugin metadata for current plugin process.

        Raises:
            IDError: No plug-in uuid found for current python process.

        Returns:
            PluginMeta: Plug-in metadata.
        """

        if not self.uuid():
            raise IDError('No plug-in uuid found for current python process.')

        return PluginMeta(self.data().plugin_id)

    # Deprecated methods.
    # TODO: Remove at next major version.

    uuid = deprecated(process_id, reason='Renamed to `process_id`')
