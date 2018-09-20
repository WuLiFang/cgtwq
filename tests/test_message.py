# -*- coding=UTF-8 -*-
"""Test module `message`.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest

import cgtwq
import util

Message = cgtwq.message.Message


def test_message_load():
    item = Message('test1测试')
    item.images.append(cgtwq.model.ImageInfo(
        max=None, min=None, path='test_image1'))
    print(item.dumps())

    item2 = Message.load(item)
    assert item2 is item

    item3 = Message.load(
        '{"image" : [{"max":null, "min":null, "path":"test_image3"}], "data" : "test3测试"}')
    assert item3 == 'test3测试'
    assert item3.images == [cgtwq.model.ImageInfo(
        max=None, min=None, path='test_image3')]

    item4 = Message.load('test4测试')
    assert item4 == 'test4测试'

    item5 = Message.load(None)
    assert item5 == ''


@util.skip_if_not_logged_in
def test_message_upload():
    cgtwq.update_setting()
    item = Message('test1测试')
    filename = util.path('resource', 'gray.png')
    item.images.append(filename)
    with pytest.raises(ValueError):
        item.dumps()
    item.upload_images('_temp', cgtwq.core.CONFIG['DEFAULT_TOKEN'])
    assert len(item.images) == 1
    assert all(isinstance(i, cgtwq.model.ImageInfo) for i in item.images)
    assert item.images[0].path == filename
    item.dumps()
