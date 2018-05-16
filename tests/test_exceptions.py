# -*- coding=UTF-8 -*-
"""Test module `cgtwq.exceptions`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

from cgtwq import exceptions


def test_template_meta():

    @six.add_metaclass(exceptions._template_meta('test', '测试'))  # pylint: disable=protected-access
    class Test(Exception):
        pass

    assert six.binary_type(Test('1')) == 'test: 1'
    assert six.text_type(Test('2')) == '测试: 2'
    assert six.binary_type(Test('1', 3)) == "test: (u'1', 3)"
    assert six.text_type(Test('1', 4)) == "测试: (u'1', 4)"
