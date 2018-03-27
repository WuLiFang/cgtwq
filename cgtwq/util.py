# -*- coding=UTF-8 -*-
"""Database in cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

from . import server
from .public_module import ACCOUNT

LOGGER = logging.getLogger(__name__)


def account_name(token=None):
    """Current user name.

    Returns:
        text_type
    """

    return ACCOUNT[server.get_account_id(token)]['name'][0]
