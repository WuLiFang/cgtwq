# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import os

from six import text_type

from ..filter import Field
from ..model import ImageInfo
from ..resultset import ResultSet
from ..server import upload
from ..server.filetools import file_md5, genreate_thumb
from .base import _OS
from .filebox import SelectionFilebox
from .history import SelectionHistory
from .link import SelectionLink
from .notify import SelectionNotify


class Selection(tuple):
    """Selection with all feature.  """
    _token = None

    def __new__(cls, module, *id_list):
        # pylint: disable=unused-argument
        if not id_list:
            raise ValueError('Empty selection.')
        assert all(isinstance(i, text_type) for i in id_list), id_list
        return super(Selection, cls).__new__(cls, id_list)

    def __init__(self, module, *id_list):
        """
        Args:
            module (Module): Related module.
            *id_list: Selected id.
        """
        # pylint: disable=unused-argument

        super(Selection, self).__init__()
        from ..module import Module
        assert isinstance(module, Module)
        self.module = module

        # Attachment.
        self.filebox = SelectionFilebox(self)
        self.history = SelectionHistory(self)
        self.link = SelectionLink(self)
        self.notify = SelectionNotify(self)

    def __getitem__(self, name):
        if isinstance(name, int):
            return super(Selection, self).__getitem__(name)
        return self.get_fields(name).column(name)

    def __setitem__(self, name, value):
        assert isinstance(name, (text_type, str))
        self.set_fields(**{name: value})

    @property
    def token(self):
        """User token.   """

        return self._token or self.module.token

    @token.setter
    def token(self, value):
        self._token = value

    def call(self, *args, **kwargs):
        """Call on this selection.   """

        kwargs.setdefault('token', self.token)
        return self.module.call(*args, id_array=self, **kwargs)

    def filter(self, filters):
        """Filter selection again.

        Args:
            filters (Filter,FilterList): Addtional filters.

        Returns:
            Selction: Filtered selection.
        """

        return self.module.filter((Field('id') | self) & filters)

    def get_fields(self, *fields):
        """Get field information for the selection.

        Args:
            *fields: Server defined field sign.

        Returns:
            ResultSet: Optimized tuple object contains fields data.
        """

        server_fields = [self.module.field(i) for i in fields]
        resp = self.call("c_orm", "get_in_id",
                         sign_array=server_fields,
                         order_sign_array=server_fields)
        return ResultSet(server_fields, resp.data, self.module)

    def set_fields(self, **data):
        """Set field data for the selection.

        Args:
            **data: Field name as key, Value as value.
        """

        data = {
            self.module.field(k): v for k, v in data.items()
        }
        resp = self.call("c_orm", "set_in_id",
                         sign_data_array=data)
        if resp.code == 0:
            raise ValueError(resp)

    def delete(self):
        """Delete the selected item on database.  """

        self.call("c_orm", "del_in_id")

    def set_image(self, path, field='image', http_server=None):
        """Set image for the field.

        Args:
            field (text_type): Defaults to 'image', Server defined field name,
            path (text_type): File path.
            http_server (text_type, optional): Defaults to None. Http server address,
                if `http_server` is None, will use value from client.
        """

        select = self
        pathname = "/upload/image/{}/".format(
            select.module.database.name
        )

        data = {'path': path}
        # Exactly same with CGTeamwork UI resolution.
        for key, width, height in (('min', 160, 120), ('max', 308, 186)):
            thumb = genreate_thumb(path, width, height)
            try:
                thumb_pathname = '{}{}.jpg'.format(pathname, file_md5(thumb))
                upload(thumb, thumb_pathname,
                       select.token, ip=http_server)
            finally:
                os.remove(thumb)
            data[key] = thumb_pathname

        select.set_fields(**{field: data})

    def get_image(self, field='image'):
        """Get imageinfo used on the field.

        Args:
            field (text_type): Defaults to 'image', Server defined field name,

        Returns:
            set[ImageInfo]: Image information.
        """

        select = self
        ret = set()
        for i in select[field]:
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

    def get_folder(self, *sign_list):
        """Get signed folder path.

        Args:
            sign_list (text_type): Sign name defined in CGTeemWork:
                `设置` -> `目录文件` -> `标识`

        Returns:
            dict: Server returned path dictionary.
                id as key, path as value.
        """

        select = self

        resp = select.call(
            "c_folder", "get_replace_path_in_sign",
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

        select = self
        select.call(
            "c_work_flow", "submit",
            task_id=select[0],
            submit_file_path_array={
                'path': pathnames, 'file_path': filenames},
            text=note)

    def has_permission_on_status(self, field):
        """Return if user has permission to edit field.

        Args:
            field (str): Field name.

        Returns:
            bool
        """

        field = self.module.field(field)
        resp = self.call(
            'c_work_flow', 'is_status_field_has_permission',
            field_sign=field,
            task_id_array=self
        )
        return resp.data

    def to_entry(self):
        """Convert selection to one entry.

        Raises:
            ValueError: Not exactly one selected item.

        Returns:
            Entry: Entry.
        """

        if len(self) != 1:
            raise ValueError('Need exactly one selected item.')

        from .entry import Entry
        return Entry(self.module, self[0])

    def to_entries(self):
        """Convert selection to entries.

        Returns:
            tuple[Entry]: Entries.
        """

        from .entry import Entry
        return tuple(Entry(self.module, i) for i in self)
