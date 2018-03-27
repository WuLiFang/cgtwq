# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import os

from ..model import ImageInfo
from ..server.file import upload
from ..server.filetools import file_md5, genreate_thumb
from .base import BaseSelection, _OS


class FileMixin(BaseSelection):
    """File operation on selection.  """

    def set_image(self, path, field='image', http_server=None):
        """Set image for the field.

        Args:
            field (text_type): Defaults to 'image', Server defined field name,
            path (text_type): File path.
            http_server (text_type, optional): Defaults to None. Http server address,
                if `http_server` is None, will use value from client.
        """

        pathname = "/upload/image/{}/".format(
            self.module.database.name
        )

        data = {'path': path}
        # Exactly same with CGTeamwork UI resolution.
        for key, width, height in (('min', 160, 120), ('max', 308, 186)):
            thumb = genreate_thumb(path, width, height)
            try:
                thumb_pathname = '{}{}.jpg'.format(pathname, file_md5(thumb))
                upload(thumb, thumb_pathname,
                       self.token, ip=http_server)
            finally:
                os.remove(thumb)
            data[key] = thumb_pathname

        self.set_fields(**{field: data})

    def get_image(self, field='image'):
        """Get imageinfo used on the field.

        Args:
            field (text_type): Defaults to 'image', Server defined field name,

        Returns:
            set[ImageInfo]: Image information.
        """

        ret = set()
        for i in self[field]:
            try:
                data = json.loads(i)
                assert isinstance(data, dict)
                # TODO: Remove `image_path` support at next major version.
                info = ImageInfo(max=data['max'],
                                 min=data['min'],
                                 path=data.get('path', data.get('image_path')))
                ret.add(info)
            except (TypeError, KeyError):
                continue
        return tuple(sorted(ret))

    def get_path(self, *sign_list):
        """Get signed folder path.

        Args:
            sign_list (text_type): Sign name defined in CGTeemWork:
                `设置` -> `目录文件` -> `标识`

        Returns:
            dict: Server returned path dictionary.
                id as key, path as value.
        """

        if not self:
            raise ValueError('Empty selection.')

        resp = self.call("c_folder", "get_replace_path_in_sign",
                         sign_array=sign_list,
                         task_id_array=self,
                         os=_OS)
        assert isinstance(resp.data, dict), type(resp.data)
        return dict(resp.data)

    def submit(self, pathnames=(), filenames=(), note=""):
        """Submit file to task, then change status to `Check`.

        Args:
            pathnames (tuple, optional): Defaults to (). Server pathnames.
            filenames (tuple, optional): Defaults to (). Local filenames.
            note (str, optional): Defaults to "". Submit note.
        """
        self.call(
            "c_work_flow", "submit",
            task_id=self[0],
            submit_file_path_array={
                'path': pathnames, 'file_path': filenames},
            text=note)
