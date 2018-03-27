# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import logging
import os

from six import text_type

from .server.file import upload
from .server.filetools import file_md5, genreate_thumb
from .filter import Field, Filter
from .model import (FileBoxDetail, ImageInfo, NoteInfo)
from .resultset import ResultSet

_OS = {'windows': 'win', 'linux': 'linux', 'darwin': 'mac'}.get(
    __import__('platform').system().lower())  # Server defined os string.
LOGGER = logging.getLogger(__name__)


class Selection(tuple):
    """Selection on a database module.   """

    _token = None

    def __new__(cls, module, *id_list):
        # pylint: disable=unused-argument
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
        from .module import Module
        assert isinstance(module, Module)
        self.module = module

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

    def get_filebox(self, sign=None, id_=None):
        """Get one filebox with sign or id_.

        Args:
            sign (text_type): Server defined filebox sign.
            id_ (text_type): Server filebox id,
                if given, will ignore `sign` value.

        Raises:
            ValueError: When selection is empty.
            ValueError: When insufficient argument.
            ValueError: When got empty result.

        Returns:
            FileBoxInfo: Filebox information.
        """

        if not self:
            raise ValueError('Empty selection.')

        if id_:
            resp = self.call("c_file", "filebox_get_one_with_id",
                             task_id=self[0],
                             filebox_id=id_,
                             os=_OS)
        elif sign:
            resp = self.call("c_file", "filebox_get_one_with_sign",
                             task_id=self[0],
                             sign=sign,
                             os=_OS)
        else:
            raise ValueError(
                'Need at least one of (sign, id_) to get filebox.')

        if not resp.data:
            raise ValueError('No matched filebox.')
        assert isinstance(resp.data, dict), resp
        return FileBoxDetail(**resp.data)

    def send_message(self, title, content, *to, **kwargs):
        """Send message to users.

        Args:
            title (text_type): Message title.
            content (text_type): Message content, support html.
            *to: Users that will recives message, use account_id.
            **kwargs:
                from_: Unknown effect. used in `cgtw` module.
        """
        # pylint: disable=invalid-name

        from_ = kwargs.get('from_')

        return self.call(
            'c_msg', 'send_task',
            task_id=self[0],
            account_id_array=to,
            title=title,
            content=content,
            from_account_id=from_
        )

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

    def get_notes(self):
        """Get notes on first item in the selection.

        Raises:
            ValueError: When no item selected.

        Returns:
            tuple[NoteInfo]: namedtuple about note information.
        """

        if not self:
            raise ValueError('Empty selection.')

        resp = self.call("c_note", "get_with_task_id",
                         task_id=self[0],
                         field_array=NoteInfo.fields)
        return tuple(NoteInfo(*i) for i in resp.data)

    def get_history(self, filters=None):
        """Get selection related history.
            filters (Filter or FilterList, optional): Defaults to None.
                Addtional history filters.

        Returns:
            tuple[HistoryInfo]: History records.
        """

        _filters = Filter('#task_id', self)
        if filters:
            _filters &= filters
        return self.module.get_history(_filters)

    def count_history(self, filters=None):
        """Count selection related history records.

        Args:
            filters (Filter or FilterList):
                Addtional history filters.

        Returns:
            int: Records count.
        """

        _filters = Filter('#task_id', self)
        if filters:
            _filters &= filters
        return self.module.count_history(_filters)

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

    def get_filebox_submit(self):
        resp = self.call(
            'c_file', 'filebox_get_submit_data',
            task_id=self[0],
            os=_OS)
        return resp

    def link(self, *id_list):
        """Link the selection to other items. """

        self.call(
            "c_link", "set_link_id",
            id_array=self, link_id_array=id_list)

    def unlink(self, *id_list):
        """Unlink the selection with other items.  """

        for id_ in self:
            self.call(
                "c_link", "remove_link_id",
                id=id_, link_id_array=id_list)

    def get_linked(self):
        """Get linked items for the selections.

        Returns:
            set: All linked item id.
        """

        ret = set()
        for id_ in self:
            resp = self.call("c_link", "get_link_id", id=id_)
            ret.add(resp)
        return ret

    def to_entry(self):
        """Convert selection to one entry.

        Raises:
            ValueError: Not exactly one selected item.

        Returns:
            Entry: Entry.
        """

        if len(self) != 1:
            raise ValueError('Need exactly one selected item.')

        return Entry(self.module, self[0])

    def to_entries(self):
        """Convert selection to entries.

        Returns:
            tuple[Entry]: Entries.
        """

        return tuple(Entry(self.module, i) for i in self)


class Entry(Selection):
    """A selection that only has one item.  """

    def __init__(self, module, id_):
        assert isinstance(id_, text_type), type(id_)
        super(Entry, self).__init__(module, id_)

    def __getitem__(self, name):
        if isinstance(name, int):
            return super(Entry, self).__getitem__(name)
        return self.get_fields(name)[0]

    def get_fields(self, *fields):
        """Get multiple fields.

        Returns:
            tuple: Result fields with exactly same order with `fields`.
        """

        ret = super(Entry, self).get_fields(*fields)
        assert len(ret) == 1, ret
        ret = ret[0]
        assert isinstance(ret, list), ret
        return tuple(ret)

    def get_image(self, field='image'):
        """Get imageinfo used on the field.

        Args:
            field (text_type): Defaults to 'image', Server defined field name,

        Raises:
            ValueError: when no image in the field.

        Returns:
            ImageInfo: Image information.
        """

        try:
            return self._to_selection().get_image(field)[0]
        except IndexError:
            raise ValueError('No image in this field.', field)

    def _to_selection(self):
        return Selection(self.module, *self)
