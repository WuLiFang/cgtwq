# -*- coding=UTF-8 -*-
"""Test module `cgtwq.exceptions`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

from cgtwq import exceptions

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import List, Tuple, Text


def test_template_meta():

    @six.add_metaclass(exceptions._template_meta('test', '测试'))  # pylint: disable=protected-access
    class Test(Exception):
        pass

    print(dir(Test))
    test_case = [(Test('1'), b'test: 1', '测试: 1'),
    ]  # type: List[Tuple[Test, bytes, Text]]
    if six.PY2:
        test_case.append((Test('2', 2), b"test: (u'2', 2)", "测试: (u'2', 2)"))
    else:
        test_case.append((Test('2', 2), b"test: ('2', 2)", "测试: ('2', 2)"))

    for i in test_case:
        assert six.binary_type(i[0]) == i[1] # type: ignore
        assert six.text_type(i[0]) == i[2]


def test_empty_selection_backward_compability():
    ex = exceptions.EmptySelection()
    assert isinstance(ex, ValueError)
    assert ex.args[0] == 'Empty selection.'
