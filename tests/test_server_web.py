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
    filename = util.path('resource', 'gray.png')
    result = cgtwq.server.web.upload_image(filename,
                                           'proj_big', cgtwq.core.CONFIG['DEFAULT_TOKEN'])
    assert isinstance(result, cgtwq.model.ImageInfo)
    assert result.path == filename
