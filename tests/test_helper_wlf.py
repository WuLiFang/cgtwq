# -*- coding=UTF-8 -*-
"""Test `cgtwq.helper.wlf` module.  """

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

import cgtwq.helper.wlf
import cgtwq
from tests import util


@util.skip_if_not_logged_in
def test_get_database():
    project = cgtwq.PROJECT.filter(cgtwq.Field("entity") == "SDKTEST").to_entry()
    orig_status = project["status"]
    project["status"] = "Active"
    assert (
        cgtwq.helper.wlf.get_database_by_file("sdktest_example.jpg") == "proj_sdktest"
    )

    with pytest.raises(cgtwq.helper.wlf.DatabaseError):
        cgtwq.helper.wlf.CGTWQHelper.get_database("example.jpg")

    project["status"] = orig_status
