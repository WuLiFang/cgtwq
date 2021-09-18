# -*- coding=UTF-8 -*-
"""Database on cgtw server.  """
from __future__ import absolute_import, division, print_function, unicode_literals

from ..core import ControllerGetterMixin
from ..filter import Field, FilterList
from ..model import FileBoxMeta
from . import core

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Tuple, Union
    import cgtwq
    import cgtwq.model


class DatabaseFilebox(core.DatabaseAttachment, ControllerGetterMixin):
    """Filebox feature for database."""

    def filter(self, *args):
        # type: (Union[FilterList, cgtwq.Filter]) -> Tuple[cgtwq.model.FileBoxMeta, ...]
        r"""Filter fileboxes metadata in the database.

        Args:
            \*filters (FilterList, Filter): Filters for server.

        Returns:
            tuple[FileBoxMeta]: namedtuple for ('id', 'pipeline_id', 'title')
        """

        filters = FilterList.from_arbitrary_args(*args) or FilterList(
            Field("#id").has("%")
        )
        return self._filter_model(
            "c_file",
            "get_with_filter",
            FileBoxMeta,
            filters=filters,
        )

    def get(self, id_):
        # type: (Text) -> cgtwq.model.FileBoxMeta
        r"""Get filebox metadata from the database.

        Args:
            id_ (str): Filebox id.

        Returns:
            FileboxMeta
        """

        resp = self.call(
            "c_file", "get_one_with_id", id=id_, field_array=FileBoxMeta.fields
        )
        return FileBoxMeta(*resp)

    from_id = get
