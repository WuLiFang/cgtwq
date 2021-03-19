# -*- coding=UTF-8 -*-
"""Use cgtw web api.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import mimetypes
import os
import cast_unknown as cast

from ..model import ImageInfo
from .http import post


def upload_image(filename, folder, token):
    """Upload image to server.

    Args:
        filename (str): Filename.
        folder (str): Server upload folder, usually same with project name.
        token (str): Server session token.

    Returns:
        ImageInfo: Uploaded image information.
    """

    filename = cast.text(filename)
    basename = os.path.basename(filename)
    data = post('web_upload_file',
                {'folder': folder,
                 'type': 'project',
                 'method': 'convert_image',
                 'filename': basename},
                token=token,
                files={'file':
                       (basename, open(filename, 'rb'),
                        mimetypes.guess_type(basename)[0])})
    assert isinstance(data, dict), type(data)
    data['path'] = filename
    return ImageInfo(**data)
