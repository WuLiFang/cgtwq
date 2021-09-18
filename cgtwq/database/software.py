# -*- coding=UTF-8 -*-
"""Database on cgtw server.  """
from __future__ import absolute_import, division, print_function, unicode_literals

from . import core
from ..core import ControllerGetterMixin


TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text


class DatabaseSoftware(core.DatabaseAttachment, ControllerGetterMixin):
    """Software feature for database."""

    # pylint: disable=too-few-public-methods

    def get_path(self, name):
        # type: (Text) -> Text
        """Get software path for the database.

        Args:
            name (str): Software name.

        Returns:
            str
        """

        return self.call("c_software", "get_software_path", name=name)

    def get_path_from_type(self, type_):
        # type: (Text) -> Text
        """Get software path for the database.

        Args:
            type (str): Software type.

        Returns:
            str
        """

        return self.call("c_software", "get_software_with_type", type=type_)
