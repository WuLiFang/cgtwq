# -*- coding=UTF-8 -*-
"""Test utilities.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
from unittest import skipIf

from cgtwq import CGTeamWorkClient
from wlf.env import HAS_QT

skip_if_not_logged_in = skipIf(not CGTeamWorkClient.is_logged_in(),  # pylint: disable=invalid-name
                               'CGTeamWork is not logged in.')
skip_if_no_qt = skipIf(  # pylint: disable=invalid-name
    not HAS_QT, 'Qt not installed')

ROOT = os.path.abspath(os.path.dirname(__file__))


def path(*other):
    """Get resource path.

    Returns:
        six.text_type: Joined absolute path.
    """

    return os.path.abspath(os.path.join(ROOT, *other))
