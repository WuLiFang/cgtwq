# -*- coding=UTF-8 -*-
"""Database on cgtw server.  """
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from deprecated import deprecated

from .. import core, server
import cast_unknown as cast
from ..filter import Field, FilterList
from ..model import ModuleInfo
from ..module import Module
from .field import DatabaseField
from .filebox import DatabaseFilebox
from .meta import DatabaseMeta
from .pipeline import DatabasePipeline
from .software import DatabaseSoftware

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Text, Union, Tuple
    import cgtwq
    import cgtwq.model


LOGGER = logging.getLogger(__name__)


class Database(core.ControllerGetterMixin):
    """Database on server."""

    # pylint: disable=too-many-instance-attributes

    _token = None

    def __init__(self, name):
        # type: (Text) -> None
        self.name = name
        self.metadata = DatabaseMeta(database=self, is_user=False)
        self.userdata = DatabaseMeta(database=self, is_user=True)

        # Attachment
        self.filebox = DatabaseFilebox(self)
        self.field = DatabaseField(self)
        self.pipeline = DatabasePipeline(self)
        self.software = DatabaseSoftware(self)

    def __getitem__(self, name):
        # type: (Text) -> Module
        return self.module(name)

    @property
    def token(self):
        # type: () -> Text
        """User token."""
        return self._token or cast.text(core.CONFIG["DEFAULT_TOKEN"])

    @token.setter
    def token(self, value):
        # type: (Text) -> None
        self._token = value

    def module(self, name, module_type="task"):
        # type: (Text, Text) -> Module
        """Get module in the database."""

        return Module(name=name, database=self, module_type=module_type)

    def call(self, *args, **kwargs):
        # type: (Any, *Any) -> Any
        """Call on this database."""

        kwargs.setdefault("token", self.token)
        return server.call(*args, db=self.name, **kwargs)

    def filter(self, *args):
        # type: (Union[FilterList, cgtwq.Filter]) -> Tuple[Module]
        """Filter modules in this database.

        Args:
            \\*filters (FilterList, Filter): Filters for server.

        Returns:
            tuple[Module]: Modules
        """

        filters = FilterList.from_arbitrary_args(*args) or FilterList(
            Field("module").has("%")
        )

        resp = self.call(
            "c_module",
            "get_with_filter",
            filter_array=filters,
            field_array=ModuleInfo.fields,
        )
        return tuple(self._get_module(ModuleInfo(*i)) for i in resp)

    def _get_module(self, info):
        # type: (ModuleInfo) -> Module
        assert isinstance(info, ModuleInfo)
        ret = self.module(info.name, module_type=info.type)
        ret.label = info.label
        return ret

    @deprecated(
        version="3.0.0",
        reason="Use `Database.metadata` or `Database.userdata` instead.",
    )
    def set_data(self, key, value, is_user=True):
        # type: (Text, Text, bool) -> None
        """Set additional data in this database.

        Args:
            key (text_type): Data key.
            value (text_type): Data value
            is_user (bool, optional): Defaults to True.
            If `is_user` is True, this data will be user specific.
        """

        accessor = self.userdata if is_user else self.metadata
        accessor[key] = value

    @deprecated(
        version="3.0.0",
        reason="Use `Database.metadata` or `Database.userdata` instead.",
    )
    def get_data(self, key, is_user=True):
        # type: (Text, bool) -> Text
        """Get additional data set in this database.

        Args:
            key (text_type): Data key.
            is_user (bool, optional): Defaults to True.
            If `is_user` is True, this data will be user specific.

        Returns:
            text_type: Data value.
        """

        accessor = self.userdata if is_user else self.metadata
        return accessor[key]

    @deprecated(
        version="3.0.0",
        reason="Use `Database.filebox.filter` or `Database.filebox.get` instead.",
    )
    def get_fileboxes(self, filters=None, id_=None):
        # type: (FilterList, Text) -> Tuple[cgtwq.model.FileBoxMeta, ...]
        r"""Get fileboxes in this database.

        Args:
            filters (FilterList, optional): Defaults to None. Filters to get filebox.
            id_ (text_type, optional): Defaults to None. Filebox id.

        Raises:
            ValueError: Not enough arguments.
            ValueError: No matched filebox.

        Returns:
            tuple[FileBoxMeta]: namedtuple for ('id', 'pipeline_id', 'title')
        """

        if id_:
            ret = (self.filebox.get(id_),)
        elif filters:
            filters = FilterList(filters)
            ret = self.filebox.filter(*filters)
        else:
            raise ValueError("Need at least one of (id_, filters) to get filebox.")

        return ret

    @deprecated(version="3.0.0", reason="Use `Database.field.filter` instead.")
    def get_fields(self, filters=None):
        # type: (Union[cgtwq.Filter, FilterList]) -> Tuple[cgtwq.model.FieldMeta, ...]
        """Get fields in the database.
            filters (Filter or FilterList, optional): Defaults to None. Filter.

        Returns:
            tuple[FieldMeta]: Field information.
        """

        filters = FilterList(filters or [])
        return self.field.filter(*filters)

    @deprecated(version="3.0.0", reason="Use `Database.field.filter_one` instead.")
    def get_field(self, filters):
        # type: (Union[cgtwq.Filter, FilterList]) -> cgtwq.model.FieldMeta
        """Get one field in the database.
            filters (Filter or FilterList): Filter.

        Returns:
            FieldMeta: Field information.
        """

        filters = FilterList(filters)
        return self.field.filter_one(*filters)

    @deprecated(version="3.0.0", reason="Use `Database.field.create` instead.")
    def create_field(self, sign, type_, name=None, label=None):
        # type: (Text, Text, Text, Text) -> None
        """Create new field in the module.

        Args:
            sign (str): Field sign
            type_ (str): Field type, see `core.FIELD_TYPES`.
            name (str, optional): Defaults to None. Field english name.
            label (str, optional): Defaults to None. Field chinese name.
        """

        self.field.create(sign, type_, name, label)

    @deprecated(version="3.0.0", reason="Use `Database.field.delete` instead.")
    def delete_field(self, field_id):
        # type: (Text) -> None
        """Delete field in the module.

        Args:
            id_ (str): Field id.
        """
        self.field.delete(field_id)

    @deprecated(
        version="3.0.0",
        reason="Use `Database.pipeline.filter` instead.",
    )
    def get_pipelines(self, *filters):
        # type: (FilterList) -> Tuple[cgtwq.model.PipelineInfo, ...]
        """Get piplines from database.

        Args:
            *filters (FilterList): Filter to get pipeline.

        Returns:
            tuple[PipelineInfo]: namedtuple for ('id', 'name', 'module')
        """

        return self.pipeline.filter(*filters)

    @deprecated(
        version="3.0.0", reason="Use `Database.filter` with empty args instead.`"
    )
    def modules(self):
        """All modules in this database.

        Returns:
            tuple[Module]: Modules
        """

        return self.filter()

    @deprecated(version="3.0.0", reason="Use `Database.software.get_path` instead.")
    def get_software(self, name):
        # type: (Text) -> Text
        """Get software path for this database.

        Args:
            name (text_type): Software name.

        Returns:
            path: Path set in `系统设置` -> `软件设置`.
        """

        return self.software.get_path(name)
