# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text
    from ._image_service import ImageService
    from ._compat_service import CompatService
    from ._http_client import HTTPClient


from ._image import Image
import os
import mimetypes
from ._util import TZ_CHINA
import datetime


class ImageServiceImpl:
    def __init__(self, http, compat):
        # type: (HTTPClient, CompatService) -> None
        self._http = http
        self._compat = compat

    def upload(self, database, filename):
        # type: (Text, Text) -> Image
        if self._compat.level <= self._compat.LEVEL_5_2:
            return self._upload_v5_2(database, filename)
        return self._upload_v6_1(database, filename)

    def _upload_v5_2(self, database, filename):
        # type: (Text, Text) -> Image
        basename = os.path.basename(filename)
        data = self._http.post(
            "web_upload_file",
            {
                "folder": database,
                "type": "project",
                "method": "convert_image",
                "filename": basename,
            },
            token=self._http.token.raw,
            files={
                "file": (
                    basename,
                    open(filename, "rb"),
                    mimetypes.guess_type(basename)[0],
                )
            },
        ).json()
        assert isinstance(data, dict), "unexpected data format: %s" % data
        return Image(data["max"], data["min"], data.get("attachment_id", ""))  # type: ignore

    def _upload_v6_1(self, database, filename):
        # type: (Text, Text) -> Image
        basename = os.path.basename(filename)
        mtime = os.path.getmtime(filename)
        data = self._http.post(
            "web_upload_file",
            {
                "method": "attachment_upload",
                "is_web": "Y",
                "db": database,
                "format": "image",
                "filename": basename,
                "attachment_argv": {
                    "type": "main",
                    "filename": filename,
                    "modify_time": datetime.datetime.fromtimestamp(
                        mtime, TZ_CHINA
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                },
            },
            token=self._http.token.raw,
            files={
                "file": (
                    basename,
                    open(filename, "rb"),
                    mimetypes.guess_type(basename)[0],
                )
            },
        ).json()
        assert isinstance(data, dict), "unexpected data format: %s" % data
        return Image(data["max"], data["min"], data["att_id"])  # type: ignore


def new_image_service(http, compat):
    # type: (HTTPClient, CompatService) -> ImageService
    return ImageServiceImpl(http, compat)
