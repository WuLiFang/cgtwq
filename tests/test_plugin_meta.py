# -*- coding=UTF-8 -*-
"""Test module `cgtwq.plugin_meta`."""

from __future__ import absolute_import, division, print_function, unicode_literals

import uuid

import pytest

import cgtwq
from tests import util


@pytest.fixture(name="plugin")
@util.skip_if_not_logged_in
def _plugin():
    return cgtwq.PluginMeta.filter(cgtwq.Field("name") == "测试")[0]


@util.skip_if_not_logged_in
def test_filter_plugin():
    result = cgtwq.PluginMeta.filter()
    for i in result:
        assert isinstance(i, cgtwq.PluginMeta)
    result = cgtwq.PluginMeta.filter(cgtwq.Field("name") == "测试")[0]
    assert isinstance(result, cgtwq.PluginMeta)


@util.skip_if_not_logged_in
def test_plugin_accessor(plugin):

    assert plugin.name == "测试"
    assert plugin.type == "menu"
    new_name = "{}_test".format("测试")
    plugin.name = new_name
    assert plugin.name == new_name
    plugin.name = "测试"


@util.skip_if_not_logged_in
def test_plugin_argument(plugin):

    key = uuid.uuid4().hex
    # Getter & Setter
    plugin.set_argument(key, description="test")
    assert plugin.get_argument(key).description == "test"

    # Delete
    del plugin.arguments[key]
    with pytest.raises(KeyError):
        plugin.get_argument(key)

    # Dict-like usage
    for i in ({"data": "test"}, 1, "测试"):
        plugin.arguments[key] = i
        assert plugin.arguments[key] == i
    del plugin.arguments[key]
