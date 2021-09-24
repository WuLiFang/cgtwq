# -*- coding=UTF-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import six
from cgtwq import _test


@_test.skip_if_not_logged_in
def test_list_submit_file():
    s = _test.select()
    s.flow.submit(s.flow.list_submit_file())
    files = s.flow.list_submit_file()
    assert files
    for i in files:
        assert isinstance(i, six.text_type)
