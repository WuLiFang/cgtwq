# -*- coding=UTF-8 -*-
"""Test module `cgtwq.plugin_meta`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import uuid

import pytest

import cgtwq
import util

TEST_PLUGIN_META = {'id': '9C8691BA-1CA1-4081-EED0-09BAFA388E8B',
                    'name': '上传工具',
                    'type': 'menu'}


@pytest.fixture(name='plugin')
@util.skip_if_not_logged_in
def _plugin():
    cgtwq.DesktopClient().connect()
    return cgtwq.PluginMeta(TEST_PLUGIN_META['id'])


@util.skip_if_not_logged_in
def test_filter_plugin():
    cgtwq.DesktopClient().connect()
    result = cgtwq.PluginMeta.filter()
    for i in result:
        assert isinstance(i, cgtwq.PluginMeta)
    result = cgtwq.PluginMeta.filter(
        cgtwq.Field('#id') == TEST_PLUGIN_META['id'])[0]
    assert isinstance(result, cgtwq.PluginMeta)


@util.skip_if_not_logged_in
def test_plugin_accesor(plugin):

    assert plugin.name == TEST_PLUGIN_META['name']
    assert plugin.type == TEST_PLUGIN_META['type']
    new_name = '{}_test'.format(TEST_PLUGIN_META['name'])
    plugin.name = new_name
    assert plugin.name == new_name
    plugin.name = TEST_PLUGIN_META['name']


@util.skip_if_not_logged_in
def test_plugin_argument(plugin):

    key = uuid.uuid4().hex
    # Getter & Setter
    plugin.set_argument(key, description='test')
    assert plugin.get_argument(key).description == 'test'

    # Delete
    del plugin.arguments[key]
    with pytest.raises(KeyError):
        plugin.get_argument(key)

    # Dict-like usage
    for i in ({'data': 'test'},
              1,
              '测试'):
        plugin.arguments[key] = i
        assert plugin.arguments[key] == i
    del plugin.arguments[key]
