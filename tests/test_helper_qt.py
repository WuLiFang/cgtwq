# -*- coding=UTF-8 -*-
"""Test module `cgtwq.helper.qt`.   """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest


@pytest.mark.skip('Need human interaction.')
def test_ask_login():
    print(1)
    from cgtwq.helper import qt
    print(qt.ask_login())


if __name__ == '__main__':
    test_ask_login()
