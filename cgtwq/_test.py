# -*- coding=UTF-8 -*-
"""Test utilities.  """
from __future__ import absolute_import, division, print_function, unicode_literals

import os

import pytest

from cgtwq import DesktopClient, compat, Database, Field

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Any

skip_if_not_logged_in = pytest.mark.skipif(
    not (
        os.getenv("CGTWQ_TEST_ACCOUNT")  # pylint: disable=invalid-name
        and os.getenv("CGTWQ_TEST_PASSWORD")
    )
    and not DesktopClient().is_logged_in(),
    reason="CGTeamWork is not logged in.",
)
skip_if_ci = pytest.mark.skipif(
    os.getenv("CI") == "true", reason="Not run with ci."  # pylint: disable=invalid-name
) # type: Any
skip_for_cgteamwork6 = pytest.mark.skipif(
    compat.api_level() == compat.API_LEVEL_6_1, reason="not run for cgteamwork6"
)

skip_if_desktop_client_not_running = pytest.mark.skipif(  # pylint: disable=invalid-name
    not DesktopClient().is_running(), reason="CGTeamWork desktop client not running."
)


def database():
    return Database("proj_sdktest")


def select():
    return (
        database()
        .module("shot")
        .filter(
            Field("shot.entity") == "SDKTEST_EP01_01_sc001",
            Field("task.pipeline") == "合成",
        )
    )


__dirname__ = os.path.abspath(os.path.dirname(__file__))


def workspace_path(*paths):
    # type: (Text) -> Text
    return os.path.join(os.path.dirname(__dirname__), *paths)
