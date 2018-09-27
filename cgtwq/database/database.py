# -*- coding=UTF-8 -*-
"""Database on cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

from wlf.decorators import deprecated

from .. import core, server
from ..filter import Field, FilterList
from ..model import FieldInfo, FileBoxMeta, ModuleInfo, PipelineInfo
from ..module import Module

LOGGER = logging.getLogger(__name__)


class Database(core.ControllerGetterMixin):
    """Database on server.    """

    _token = None

    def __init__(self, name):
        self.name = name
        self.metadata = DatabaseMeta(database=self, is_user=False)
        self.userdata = DatabaseMeta(database=self, is_user=True)

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

    def get_fileboxes(self, filters=None, id_=None):
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
            ret = [self.call("c_file", "get_one_with_id",
                             id=id_,
                             field_array=FileBoxMeta.fields)]
        elif filters:
            ret = self.call("c_file", "get_with_filter",
                            filter_array=FilterList(filters),
                            field_array=FileBoxMeta.fields)
        else:
            raise ValueError(
                'Need at least one of (id_, filters) to get filebox.')

        assert all(isinstance(i, list) for i in ret), ret
        return tuple(FileBoxMeta(*i) for i in ret)

    def get_pipelines(self, filters=None):
        """Get piplines from database.

        Args:
            filters (FilterList): Filter to get pipeline.

        Returns:
            tuple[PipelineInfo]: namedtuple for ('id', 'name', 'module')
        """

        filters = filters or Field('entity_name').has('%')
        return self._get_model(
            "c_pipeline", "get_with_filter",
            PipelineInfo, filters)

    def get_software(self, name):
        """Get software path for this database.

        Args:
            name (text_type): Software name.

        Returns:
            path: Path set in `系统设置` -> `软件设置`.
        """

        return self.call("c_software", "get_software_path", name=name)

    def get_fields(self, filters=None):
        """Get fields in the database.
            filters (Filter or FilterList, optional): Defaults to None. Filter.

        Returns:
            tuple[FieldInfo]: Field informations.
        """

        filters = filters or Field('sign').has('%')
        filters = FilterList(filters)
        resp = self.call(
            'c_field', 'get_with_filter',
            field_array=FieldInfo.fields,
            filter_array=filters
        )
        return tuple(FieldInfo(*i) for i in resp)

    def get_field(self, filters):
        """Get one field in the database.
            filters (Filter or FilterList): Filter.

        Returns:
            FieldInfo: Field information.
        """

        filters = FilterList(filters)
        resp = self.call(
            'c_field', 'get_one_with_filter',
            field_array=FieldInfo.fields,
            filter_array=filters
        )
        return FieldInfo(*resp)

    def create_field(self, sign, type_, name=None, label=None):
        """Create new field in the module.

        Args:
            sign (str): Field sign
            type_ (str): Field type, see `core.FIELD_TYPES`.
            name (str, optional): Defaults to None. Field english name.
            label (str, optional): Defaults to None. Field chinese name.
        """

        assert type_ in core.FIELD_TYPES,\
            'Field type must in {}'.format(core.FIELD_TYPES)
        assert '.' in sign, 'Sign must contains a `.` character to specific module.'

        module, sign = sign.split('.')
        label = label or sign
        name = name or sign

        self.call(
            "c_field", "python_create",
            module=module,
            field_str=label,
            en_name=name,
            sign=sign,
            type=type_,
            field_name=sign,
        )

    def delete_field(self, field_id):
        """Delte field in the module.

        Args:
            id_ (str): Field id.
        """
        self.call(
            'c_field', 'del_one_with_id',
            id=field_id
        )

    def filter(self, *filters):
        """Filter modules in this database.

        Args:
            *filters (FilterList, Filter): Filters for server.

        Returns:
            tuple[Module]: Modules
        """
        filters = FilterList.from_arbitrary_args(*filters)

        resp = self.call(
            'c_module', 'get_with_filter',
            filter_array=filters,
            field_array=ModuleInfo.fields
        )
        return tuple(self._get_module(ModuleInfo(*i)) for i in resp)

    def modules(self):
        """All modules in this database.

        Returns:
            tuple[Module]: Modules
        """

        return self.filter(Field('module').has('%'))

    def _get_module(self, info):
        assert isinstance(info, ModuleInfo)
        ret = self.module(info.name, module_type=info.type)
        ret.label = info.label
        return ret

    # Deprecated methods.

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
