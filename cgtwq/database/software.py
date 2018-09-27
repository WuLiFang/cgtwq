# -*- coding=UTF-8 -*-
"""Database on cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import core
from ..core import ControllerGetterMixin


class DatabaseSoftware(core.DatabaseAttachment, ControllerGetterMixin):
    """Software feature for database.  """
    # pylint: disable=too-few-public-methods

    def get_path(self, name):
        """Get software path for the database.

        Args:
            name (text_type): Software name.

        Returns:
            path: Path set in `系统设置` -> `软件设置`.
        """

        return self.call("c_software", "get_software_path", name=name)
