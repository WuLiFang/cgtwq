# -*- coding=UTF-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from cgtwq import _test, Field


@_test.skip_if_not_logged_in
def test_from_id():
    s = _test.select()
    database = s.module.database

    filebox_list = database.filebox.list_by_pipeline(
        *database.pipeline.filter(Field("entity") == "合成")
    )
    assert filebox_list
    filebox = s.filebox.from_id(filebox_list[0].id)
    assert filebox.path
