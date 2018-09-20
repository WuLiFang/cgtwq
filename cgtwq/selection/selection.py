# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json

from six import text_type

from wlf.decorators import deprecated

from ..filter import Field
from ..model import ImageInfo
from ..resultset import ResultSet
from ..server.web import upload_image
from .base import _OS
from .filebox import SelectionFilebox
from .flow import SelectionFlow
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
        self.flow = SelectionFlow(self)

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
        kwargs.setdefault('id_array', self)
        return self.module.call(*args, **kwargs)

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
        return ResultSet(server_fields, resp, self.module)

    def set_fields(self, **data):
        """Set field data for the selection.

        Args:
            **data: Field name as key, Value as value.
        """

        data = {
            self.module.field(k): v for k, v in data.items()
        }
        self.call("c_orm", "set_in_id",
                  sign_data_array=data)

    def delete(self):
        """Delete the selected item on database.  """

        self.call("c_orm", "del_in_id")

    def set_image(self, path, field='image'):
        """Set image for the field.

        Args:
            field (text_type): Defaults to 'image', Server defined field name,
            path (text_type): File path.

        Returns:
            ImageInfo: Uploaded image.
        """
        image = upload_image(path, self.module.database.name, self.token)

        # Server need strange data format for image field in cgteamwork5.2
        self.set_fields(
            **{field: dict(path=path, max=[image.max], min=[image.min])})
        return image

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
                info = ImageInfo(max=data['max'][0],
                                 min=data['min'][0],
                                 path=data.get('path'))
                ret.add(info)
            except (TypeError, KeyError):
                continue
        return tuple(sorted(ret))

    def get_folder(self, *sign_list):
        """Get signed folder path.

        Args:
            sign_list (text_type): Sign name defined in CGTeemWork:
                `项目设置` -> `目录文件` -> `标识`

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
        assert isinstance(resp, dict), type(resp)
        return resp

    def _submit(self, pathnames=(), filenames=(), note=""):
        """Submit file to task, then change status to `Check`.

        Args:
            pathnames (tuple, optional): Defaults to (). Server pathnames.
            filenames (tuple, optional): Defaults to (). Local filenames.
            note (str, optional): Defaults to "". Submit note.
        """

        # TODO: Remove at next major version.
        self.flow.submit(pathnames + filenames, message=note)

    submit = deprecated(_submit, 'Use `Selection.flow.submit` insted.')

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
        return resp

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

    @classmethod
    def from_data(cls, **kwargs):
        """Get selection from dictionary-like data.

        Arguments:
            **kwargs:
                database(str): Databse name.
                module(str): Module name.
                module_type(str): Module type.
                id_list(list): Id list.
        """

        from ..database import Database
        return Database(
            kwargs['database']
        ).module(
            kwargs['module'], module_type=kwargs['module_type']
        ).select(*kwargs['id_list'])
