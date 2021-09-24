# -*- coding=UTF-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import cgtwq
import six
from cgtwq import _test


def _select():
    return (
        cgtwq.Database("proj_sdktest")
        .module("shot")
        .filter(
            cgtwq.Field("shot.entity") == "SDKTEST_EP01_01_sc001",
            cgtwq.Field("task.pipeline") == "合成",
        )
    )


@_test.skip_if_not_logged_in
def test_list_submit_file():
    s = _select()
    s.flow.submit(s.flow.list_submit_file())
    files = s.flow.list_submit_file()
    assert files
    for i in files:
        assert isinstance(i, six.text_type)
