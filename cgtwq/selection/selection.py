# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import absolute_import, division, print_function, unicode_literals

import six
from deprecated import deprecated

from ..exceptions import EmptySelection
from ..filter import Field
from ..resultset import ResultSet
from .core import _OS
from .filebox import SelectionFilebox
from .flow import SelectionFlow
from .folder import SelectionFolder
from .history import SelectionHistory
from .image import SelectionImage
from .link import SelectionLink
from .notify import SelectionNotify
from .pipeline import SelectionPipeline

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Dict, Text, Tuple, Union, overload

    import cgtwq
    import cgtwq.model


class Selection(tuple):
    """Selection with all feature.

    Raises:
        EmptySelection: when selection size is 0.
    """

    # pylint: disable=too-many-instance-attributes
    _token = None

    def __new__(cls, module, *id_list):
        # type: (cgtwq.Module, Text) -> Selection
        # pylint: disable=unused-argument
        if not id_list:
            raise EmptySelection()
        assert all(isinstance(i, six.text_type) for i in id_list), id_list
        return super(Selection, cls).__new__(cls, id_list)

    def __init__(self, module, *id_list):
        # type: (cgtwq.Module, Text) -> None
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
        self.image = SelectionImage(self)
        self.pipeline = SelectionPipeline(self)
        self.folder = SelectionFolder(self)

    if TYPE_CHECKING:

        @overload
        def __getitem__(self, name):
            # type: (int) -> Text
            raise NotImplementedError()

        @overload
        def __getitem__(self, name):
            # type: (Text) -> Tuple[Any, ...]
            raise NotImplementedError()

    def __getitem__(self, name):
        # type: (Union[Text, int]) -> Union[Tuple[Any, ...], Text]
        if isinstance(name, int):
            return super(Selection, self).__getitem__(name)
        return self.get_fields(name).column(name)

    def __setitem__(self, name, value):
        # type: (Text, Any) -> None
        assert isinstance(name, (six.text_type, str))
        self.set_fields(**{name: value})

    @property
    def token(self):
        # type: () -> Text
        """User token."""

        return self._token or self.module.token

    @token.setter
    def token(self, value):
        # type: (Text) -> None
        self._token = value

    def call(self, *args, **kwargs):
        # type: (Any, *Any) -> Any
        """Call on this selection."""

        kwargs.setdefault("token", self.token)
        kwargs.setdefault("id_array", self)
        kwargs.setdefault("task_id_array", self)
        return self.module.call(*args, **kwargs)

    def filter(self, *filters):
        # type: (Union[cgtwq.Filter, cgtwq.FilterList]) -> Selection
        r"""Filter selection again.

        Args:
            \*filters (Filter,FilterList): Additional filters.

        Returns:
            Selection: Filtered selection.
        """

        return self.module.filter(Field("id").in_(self), *filters)

    def count(self, *filters):
        # type: (Union[cgtwq.Filter, cgtwq.FilterList]) -> int
        r"""Count matched entity in the selection.

        Args:
            \*filters (Filter,FilterList): Filters.

        Returns:
            int: Count value.
        """

        return self.module.count(Field("id").in_(self), *filters)

    def distinct(self, *filters, **kwargs):
        # type: (Union[cgtwq.Filter,cgtwq.FilterList], *Any) -> Tuple[Any, ...]
        r"""Get distinct value in the selection.

        Args:
            \*filters (FilterList, Filter): Filters for server.
            \*\*kwargs:

        \*\*kwargs:
            key: Distinct key, defaults to field of first filter.

        Returns:
            tuple
        """

        return self.module.distinct(Field("id").in_(self), *filters, **kwargs)

    def get_fields(self, *fields, **kwargs):
        # type: (Text, *Any) -> ResultSet
        r"""Get field information for the selection.

        Args:
            \*fields: Server defined field sign.
            \*\*kwargs:

        \*\*kwargs:
            namespace (str, optional): Default namespace for key.

        Returns:
            ResultSet: Optimized tuple object contains fields data.
        """

        namespace = kwargs.pop("namespace", self.module.default_field_namespace)

        server_fields = [Field(i).in_namespace(namespace) for i in fields]
        resp = self.call(
            "c_orm",
            "get_in_id",
            sign_array=server_fields,
            order_sign_array=server_fields,
        )
        return ResultSet(server_fields, resp, self.module)

    def set_fields(self, kwargs=None, **data):
        # type: (Dict[Text, Any], *Any) -> None
        r"""Set field data for the selection.

        Args:
            kwargs (dict):
            \*\*data: Field name as key, Value as value.

        kwargs:
            namespace (str, optional): Default namespace for key.
        """

        kwargs = kwargs or dict()
        namespace = kwargs.pop("namespace", self.module.default_field_namespace)

        data = {Field(k).in_namespace(namespace): v for k, v in data.items()}
        self.call("c_orm", "set_in_id", sign_data_array=data)

    def delete(self):
        """Delete the selected item on database."""

        self.call("c_orm", "del_in_id")

    def get_folder(self, *sign_list):
        # type: (Text) -> Dict[Text, Text]
        """Get signed folder path.

        Args:
            sign_list (six.text_type): Sign name defined in CGTeemWork:
                `项目设置` -> `目录文件` -> `标识`

        Returns:
            dict: Server returned path dictionary.
                id as key, path as value.
        """

        select = self

        resp = select.call(
            "c_folder",
            "get_replace_path_in_sign",
            sign_array=sign_list,
            task_id_array=self,
            os=_OS,
        )
        assert isinstance(resp, dict), type(resp)
        return resp

    def to_entry(self):
        # type: () -> cgtwq.Entry
        """Convert selection to one entry.

        Raises:
            ValueError: Not exactly one selected item.

        Returns:
            Entry: Entry.
        """

        if len(self) != 1:
            raise ValueError("Need exactly one selected item.")

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
        # type: (*Any) -> cgtwq.Selection
        r"""Get selection from dictionary-like data.

        Arguments:
            \*\*kwargs:
                database(str): Database name.
                module(str): Module name.
                module_type(str): Module type.
                id_list(list): Id list.
        """

        from ..database import Database

        return (
            Database(kwargs["database"])
            .module(kwargs["module"], module_type=kwargs["module_type"])
            .select(*kwargs["id_list"])
        )

    @deprecated(version="3.0.0", reason="Use `Selection.flow.submit` insted.")
    def submit(self, pathnames=(), filenames=(), note=""):
        # type: (Tuple[Text, ...], Tuple[Text, ...], Text) -> None
        """Submit file to task, then change status to `Check`.

        Args:
            pathnames (tuple, optional): Defaults to (). Server pathnames.
            filenames (tuple, optional): Defaults to (). Local filenames.
            note (str, optional): Defaults to "". Submit note.
        """

        self.flow.submit(pathnames + filenames, message=note)

    @deprecated(version="3.0.0", reason="Use `Selection.image.set` insted.")
    def set_image(self, path, field="image"):
        # type: (Text, Text) -> cgtwq.model.ImageInfo
        """Set image for the field.

        Args:
            field (six.text_type): Defaults to 'image', Server defined field name,
            path (six.text_type): File path.

        Returns:
            ImageInfo: Uploaded image.
        """
        return self.image.set(path, field)

    @deprecated(
        version="3.0.0",
        reason="Use `Selection.image.get` insted.",
    )
    def get_image(self, field="image"):
        # type: (Text) -> Tuple[cgtwq.model.ImageInfo, ...]
        """Get imageinfo used on the field.

        Args:
            field (six.text_type): Defaults to 'image', Server defined field name,

        Returns:
            set[ImageInfo]: Image information.
        """

        return self.image.get(field)

    @deprecated(
        version="3.0.0",
        reason="Use `Selection.flow.has_field_permission` Instead",
    )
    def has_permission_on_status(self, field):
        # type: (Text) -> bool
        """Return if user has permission to edit field.

        Args:
            field (str): Field name.

        Returns:
            bool
        """

        return self.flow.has_field_permission(field)
