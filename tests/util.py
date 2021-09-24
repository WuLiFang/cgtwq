# -*- coding=UTF-8 -*-
"""Test utilities.  """
from __future__ import absolute_import, division, print_function, unicode_literals

import os

from cgtwq._test import (
    skip_for_cgteamwork6,
    skip_if_not_logged_in,
    skip_if_desktop_client_not_running,
    skip_if_ci,
)


ROOT = os.path.abspath(os.path.dirname(__file__))


def path(*other):
    """Get resource path.

    Returns:
        six.text_type: Joined absolute path.
    """

    return os.path.abspath(os.path.join(ROOT, *other))


__all__ = [
    "skip_for_cgteamwork6",
    "skip_if_not_logged_in",
    "skip_if_desktop_client_not_running",
    "skip_if_ci",
    "path",
    "ROOT",
]
