# -*- coding=UTF-8 -*-
"""Connect to CGTeamWork official gui client.  """

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

if sys.platform == "win32":
    from .client import DesktopClient
else:
    from .dummy import DesktopClient

__all__ = ["DesktopClient"]
