# -*- coding=UTF-8 -*-
"""Test `server.web` module.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import cgtwq
import cgtwq.server.web
import util


@util.skip_if_not_logged_in
def test_upload_image():
    cgtwq.update_setting()
    resp = cgtwq.server.web.upload_image(util.path('resource', 'gray.png'),
                                         'proj_big', cgtwq.server.setting.DEFAULT_TOKEN)
    print(resp)
