# -*- coding=UTF-8 -*-
"""Test module `account`.  """

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import uuid

import cgtwq
import cgtwq.account
import pytest

from tests import util


@util.skip_if_not_logged_in
@pytest.mark.skipif(
    not (os.getenv("CGTWQ_TEST_ACCOUNT") and os.getenv("CGTWQ_TEST_PASSWORD")),
    reason="Need a test account",
)
def test_login():
    cgtwq.account.login(
        os.getenv("CGTWQ_TEST_ACCOUNT") or "", os.getenv("CGTWQ_TEST_PASSWORD") or ""
    )


@util.skip_if_not_logged_in
def test_login_fail():
    with pytest.raises(cgtwq.AccountNotFoundError):
        cgtwq.account.login(uuid.uuid4().hex, "")
    with pytest.raises(cgtwq.PasswordError):
        cgtwq.account.login("admin", uuid.uuid4().hex)
