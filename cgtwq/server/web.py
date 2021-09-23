# -*- coding=UTF-8 -*-
"""Use cgtw web api.  """

from __future__ import absolute_import, division, print_function, unicode_literals

import mimetypes
import os
import cast_unknown as cast

from ..model import ImageInfo
from .http import post
import datetime
from .. import compat

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text


class ChinaTimezone(datetime.tzinfo):
    """Timezone of china."""

    def tzname(self, dt):
        return "UTC+8"

    def utcoffset(self, dt):
        return datetime.timedelta(hours=8)

    def dst(self, dt):
        return datetime.timedelta()


def _upload_image_v5_2(filename, folder, token):
    # type: (Text, Text, Text) -> ImageInfo
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
    data = post(
        "web_upload_file",
        {
            "folder": folder,
            "type": "project",
            "method": "convert_image",
            "filename": basename,
        },
        token=token,
        files={
            "file": (basename, open(filename, "rb"), mimetypes.guess_type(basename)[0])
        },
    )
    assert isinstance(data, dict), type(data)
    return ImageInfo(data["min"], data["max"], filename)


def _upload_image_v6_1(filename, folder, token):
    # type: (Text, Text, Text) -> ImageInfo
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
    mtime = os.path.getmtime(filename)
    data = post(
        "web_upload_file",
        {
            "method": "attachment_upload",
            "is_web": "Y",
            "db": folder,
            "format": "image",
            "filename": basename,
            "attachment_argv": {
                "type": "main",
                "filename": filename,
                "modify_time": datetime.datetime.fromtimestamp(
                    mtime, ChinaTimezone()
                ).strftime("%Y-%m-%d %H:%M:%S"),
            },
        },
        token=token,
        files={
            "file": (basename, open(filename, "rb"), mimetypes.guess_type(basename)[0])
        },
    )
    assert isinstance(data, dict), type(data)
    return ImageInfo(data["min"], data["max"], filename, data["att_id"])


def upload_image(filename, folder, token):
    # type: (Text, Text, Text) -> ImageInfo

    if compat.api_level() == compat.API_LEVEL_5_2:
        return _upload_image_v5_2(filename, folder, token)
    return _upload_image_v6_1(filename, folder, token)
