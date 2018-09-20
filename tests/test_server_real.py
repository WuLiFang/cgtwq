# -*- coding=UTF-8 -*-
"""Test module `cgtwq.database`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import cgtwq
from util import skip_if_not_logged_in


@skip_if_not_logged_in
def test_account():
    account = cgtwq.get_account()
    account_id = cgtwq.get_account_id()
    print('# account: <id: {}: {}>'.format(account_id, account))
