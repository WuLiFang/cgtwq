# -*- coding=UTF-8 -*-
"""Test module `cgtwq.database`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import util
import cgtwq


@util.skip_if_not_logged_in
def test_module_fileds():
    cgtwq.update_setting()
    module = cgtwq.Database('proj_mt').module('shot_task')
    result = module.get_fields()
    print(result)
