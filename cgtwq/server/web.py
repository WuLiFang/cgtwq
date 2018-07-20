# -*- coding=UTF-8 -*-
"""Use cgtw web api.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import mimetypes
import os

from wlf.codectools import get_encoded as e
from wlf.codectools import get_unicode as u

from .http import post


def upload_image(filename, folder, token):
    """Upload image to server.  """

    filename = u(filename)
    basename = os.path.basename(filename)
    return post('web_upload_file',
                {'folder': folder,
                 'type': 'project',
                 'method': 'convert_image',
                 'filename': basename},
                token=token,
                files={'file':
                       (basename, open(e(filename), 'rb'),
                        mimetypes.guess_type(basename)[0])})
