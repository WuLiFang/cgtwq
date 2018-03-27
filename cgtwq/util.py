# -*- coding=UTF-8 -*-
"""CGTeamWork utility.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import hashlib
import os
from tempfile import mkstemp

from wlf.ffmpeg import _try_run_cmd


def genreate_thumb(path, width, height):
    """Generate thumb for image.
        will padding black border to keep aspect ratio.

    Args:
        path (unicode): Image path.

    Returns:
        unicode: Generated thumb path.
    """

    fd, filename = mkstemp('.jpg')

    # Generate.
    cmd = ('ffmpeg -y -hide_banner '
           '-i "{input}" '
           '-vf scale=trunc({width}/2)*2:trunc({height}/2)*2:'
           'force_original_aspect_ratio=decrease,'
           'pad={width}:{height}:abs(ow-iw)/2:abs(oh-ih)/2,setsar=1 '
           '-q:v 1 '
           '"{output}"').format(input=path, output=filename,
                                width=width, height=height)

    _try_run_cmd(cmd, 'Error during generate thumb')
    os.close(fd)

    return filename


def file_md5(path):
    """Get md5 from path.

    Args:
        path (unicode): File path.

    Returns:
        unicode: Hexdigest of file.
    """

    hash_ = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(2048), b''):
            hash_.update(chunk)
    return hash_.hexdigest()
