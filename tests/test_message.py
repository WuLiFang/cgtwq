# -*- coding=UTF-8 -*-
"""Test module `message`.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from cgtwq.message import Message


def test_message():
    item = Message('test1测试')
    item.images.append('test_image1')
    print(item.dumps())

    item2 = Message.load(item)
    assert item2 is item

    item3 = Message.load('{"image" : ["test_image3"], "data" : "test3测试"}')
    assert item3 == 'test3测试'
    assert item3.images == ['test_image3']

    item4 = Message.load('test4测试')
    assert item4 == 'test4测试'

    item5 = Message.load(None)
    assert item5 == ''
