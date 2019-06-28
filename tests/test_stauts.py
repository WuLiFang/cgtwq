# -*- coding=UTF-8 -*-
"""Test module `cgtwq.status`.   """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import cgtwq
from tests import util


@util.skip_if_not_logged_in
def test_get_status():
    print(cgtwq.server.meta.get_status())
