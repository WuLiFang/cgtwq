# -*- coding=UTF-8 -*-
"""Database on cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

from wlf.decorators import deprecated

from .. import core, server
from ..filter import Field, FilterList
from ..model import ModuleInfo
from ..module import Module
from .field import DatabaseField
from .filebox import DatabaseFilebox
from .pipeline import DatabasePipeline
from .software import DatabaseSoftware

LOGGER = logging.getLogger(__name__)


class Database(core.ControllerGetterMixin):
    """Database on server.    """

    _token = None

    def __init__(self, name):
        self.name = name
        self.metadata = DatabaseMeta(database=self, is_user=False)
        self.userdata = DatabaseMeta(database=self, is_user=True)

        # Attachment
        self.filebox = DatabaseFilebox(self)
        self.field = DatabaseField(self)
        self.pipeline = DatabasePipeline(self)
        self.software = DatabaseSoftware(self)

    def __getitem__(self, name):
        return self.module(name)

    @property
    def token(self):
        """User token.   """
        return self._token or core.CONFIG['DEFAULT_TOKEN']

    @token.setter
    def token(self, value):
        self._token = value

    def module(self, name, module_type='task'):
        """Get module in the database.  """

        return Module(name=name, database=self, module_type=module_type)

    def call(self, *args, **kwargs):
        """Call on this database.   """

        kwargs.setdefault('token', self.token)
        return server.call(*args, db=self.name, **kwargs)

    def filter(self, *filters):
        """Filter modules in this database.

        Args:
            *filters (FilterList, Filter): Filters for server.

        Returns:
            tuple[Module]: Modules
        """

        filters = (FilterList.from_arbitrary_args(*filters)
                   or FilterList(Field('module').has('%')))

        resp = self.call(
            'c_module', 'get_with_filter',
            filter_array=filters,
            field_array=ModuleInfo.fields
        )
        return tuple(self._get_module(ModuleInfo(*i)) for i in resp)

    def _get_module(self, info):
        assert isinstance(info, ModuleInfo)
        ret = self.module(info.name, module_type=info.type)
        ret.label = info.label
        return ret

    # Deprecated methods.
    # TODO: Remove at next major version.

    def _set_data(self, key, value, is_user=True):
        """Set addtional data in this database.

        Args:
            key (text_type): Data key.
            value (text_type): Data value
            is_user (bool, optional): Defaults to True.
                If `is_user` is True, this data will be user specific.
        """

        accessor = self.userdata if is_user else self.metadata
        accessor[key] = value

    set_data = deprecated(
        _set_data,
        reason='Use `Database.metadata` or `Database.userdata` instead.')

    def _get_data(self, key, is_user=True):
        """Get addional data set in this database.

        Args:
            key (text_type): Data key.
            is_user (bool, optional): Defaults to True.
                If `is_user` is True, this data will be user specific.

        Returns:
            text_type: Data value.
        """

        accessor = self.userdata if is_user else self.metadata
        return accessor[key]

    get_data = deprecated(
        _get_data,
        reason='Use `Database.metadata` or `Database.userdata` instead.')

    def _get_fileboxes(self, filters=None, id_=None):
        """Get fileboxes in this database.
            filters (FilterList, optional): Defaults to None. Filters to get filebox.
            id_ (text_type, optional): Defaults to None. Filebox id.

        Raises:
            ValueError: Not enough arguments.
            ValueError: No matched filebox.

        Returns:
            tuple[FileBoxCategoryInfo]: namedtuple for ('id', 'pipeline_id', 'title')
        """

        if id_:
            ret = [self.filebox.get(id_)]
        elif filters:
            filters = FilterList(filters)
            ret = self.filebox.filter(*filters)
        else:
            raise ValueError(
                'Need at least one of (id_, filters) to get filebox.')

        return ret

    get_fileboxes = deprecated(
        _get_fileboxes,
        reason='Use `Database.filebox.filter` or `Database.filebox.get` instead.')

    def _get_fields(self, filters=None):
        """Get fields in the database.
            filters (Filter or FilterList, optional): Defaults to None. Filter.

        Returns:
            tuple[FieldInfo]: Field informations.
        """

        filters = filters or []
        filters = FilterList(filters)
        return self.field.filter(*filters)

    get_fields = deprecated(
        _get_fields,
        reason='Use `Database.field.filter` instead.')

    def _get_field(self, filters):
        """Get one field in the database.
            filters (Filter or FilterList): Filter.

        Returns:
            FieldInfo: Field information.
        """

        filters = FilterList(filters)
        return self.field.filter_one(*filters)

    get_field = deprecated(
        _get_field,
        reason='Use `Database.field.filter_one` instead.')

    def _create_field(self, sign, type_, name=None, label=None):
        """Create new field in the module.

        Args:
            sign (str): Field sign
            type_ (str): Field type, see `core.FIELD_TYPES`.
            name (str, optional): Defaults to None. Field english name.
            label (str, optional): Defaults to None. Field chinese name.
        """

        self.field.create(sign, type_, name, label)

    create_field = deprecated(
        _create_field,
        reason='Use `Database.field.create` instead.')

    def _delete_field(self, field_id):
        """Delte field in the module.

        Args:
            id_ (str): Field id.
        """
        self.field.delete(field_id)

    delete_field = deprecated(
        _delete_field,
        reason='Use `Database.field.delete` instead.')

    def _get_pipelines(self, *filters):
        """Get piplines from database.

        Args:
            *filters (FilterList): Filter to get pipeline.

        Returns:
            tuple[PipelineInfo]: namedtuple for ('id', 'name', 'module')
        """

        return self.pipeline.filter(*filters)

    get_pipelines = deprecated(
        _get_pipelines,
        reason='Use `Database.pipeline.filter` instead.')

    def _modules(self):
        """All modules in this database.

        Returns:
            tuple[Module]: Modules
        """

        return self.filter()

    modules = deprecated(
        _modules,
        reason='Use `Database.filter` with empty args instead.`'
    )

    def _get_software(self, name):
        """Get software path for this database.

        Args:
            name (text_type): Software name.

        Returns:
            path: Path set in `系统设置` -> `软件设置`.
        """

        return self.software.get_path(name)

    get_software = deprecated(
        _get_software,
        reason='Use `Database.software.get_path` instead.'
    )


class DatabaseMeta(object):
    """Database metadate accessor.  """
    # pylint: disable=too-few-public-methods

    def __init__(self, database, is_user):
        self.database = database
        self.is_user = is_user

    def __getitem__(self, key):
        return self.database.call(
            "c_api_data",
            'get_user' if self.is_user else 'get_common',
            key=key)

    def __setitem__(self, key, value):
        self.database.call(
            "c_api_data",
            'set_user' if self.is_user else 'set_common',
            key=key, value=value)
