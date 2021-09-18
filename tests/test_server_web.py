# -*- coding=UTF-8 -*-
"""Test `server.web` module.  """

from __future__ import absolute_import, division, print_function, unicode_literals

import cgtwq.core
import cgtwq.model
import cgtwq.server.web

from tests import util


@util.skip_if_not_logged_in
def test_upload_image():
    filename = util.path("resource", "gray.png")
    result = cgtwq.server.web.upload_image(
        filename, "proj_sdktest", cgtwq.core.CONFIG["DEFAULT_TOKEN"]
    )
    assert isinstance(result, cgtwq.model.ImageInfo)
    assert result.path == filename
