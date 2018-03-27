# -*- coding=UTF-8 -*-
"""Database on cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

from . import server
from .filter import FilterList
from .model import (FIELDS_FILEBOX, FIELDS_HISTORY, FIELDS_NOTE,
                    FIELDS_PIPELINE, FileBoxDetail, FileBoxInfo, HistoryInfo,
                    ImageInfo, NoteInfo, PipelineInfo)
from .module import Module
from .server import setting

LOGGER = logging.getLogger(__name__)


class Database(object):
    """Database on server.    """

    _token = None

    def __init__(self, name):
        self.name = name

    def call(self, *args, **kwargs):
        """Call on this database.   """

        kwargs.setdefault('token', self.token)
        return server.call(*args, db=self.name, **kwargs)

    def __getitem__(self, name):
        return Module(name=name, database=self)

    @property
    def token(self):
        """User token.   """
        return self._token or setting.DEFAULT_TOKEN

    @token.setter
    def token(self, value):
        self._token = value

    def get_fileboxes(self, filters=None, id_=None):
        """Get fileboxes in this database.
            filters (FilterList, optional): Defaults to None. Filters to get filebox.
            id_ (text_type, optional): Defaults to None. Filebox id.

        Raises:
            ValueError: Not enough arguments.
            ValueError: No matched filebox.

        Returns:
            tuple[Filebox]: namedtuple for ('id', 'pipeline_id', 'title')
        """

        if id_:
            resp = self.call("c_file", "get_one_with_id",
                             id=id_,
                             field_array=FIELDS_FILEBOX)
            ret = [resp.data]
        elif filters:
            resp = self.call("c_file", "get_with_filter",
                             filter_array=FilterList(filters),
                             field_array=FIELDS_FILEBOX)
            ret = resp.data
        else:
            raise ValueError(
                'Need at least one of (id_, filters) to get filebox.')

        if not resp.data:
            raise ValueError('No matched filebox.')
        assert all(isinstance(i, list) for i in ret), resp
        return tuple(FileBoxInfo(*i) for i in ret)

    def get_piplines(self, filters):
        """Get piplines from database.

        Args:
            filters (FilterList): Filter to get pipeline.

        Returns:
            tuple[Pipeline]: namedtuple for ('id', 'name', 'module')
        """

        resp = self.call(
            "c_pipeline", "get_with_filter",
            field_array=FIELDS_PIPELINE,
            filter_array=FilterList(filters))
        return tuple(PipelineInfo(*i) for i in resp.data)

    def get_software(self, name):
        """Get software path for this database.

        Args:
            name (text_type): Software name.

        Returns:
            path: Path set in `设置` -> `软件`.
        """

        resp = self.call("c_software", "get_path", name=name)
        return resp.data

    def set_data(self, key, value, is_user=True):
        """Set addtional data in this database.

        Args:
            key (text_type): Data key.
            value (text_type): Data value
            is_user (bool, optional): Defaults to True.
                If `is_user` is True, this data will be user specific.
        """

        self.call("c_api_data",
                  'set_user' if is_user else 'set_common',
                  key=key, value=value)

    def get_data(self, key, is_user=True):
        """Get addional data set in this database.

        Args:
            key (text_type): Data key.
            is_user (bool, optional): Defaults to True.
                If `is_user` is True, this data will be user specific.

        Returns:
            text_type: Data value.
        """

        resp = self.call("c_api_data",
                         'get_user' if is_user else 'get_common',
                         key=key)
        return resp.data
