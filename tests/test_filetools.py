# -*- coding=UTF-8 -*-
"""Test module `cgtwq.filetools`.   """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import sys
from unittest import TestCase, main, skipIf

import six

import util


from cgtwq.filetools import genreate_thumb


class FileToolsTestCase(TestCase):

    @skipIf(six.PY3, 'TODO')
    @skipIf(sys.platform != 'win32', 'TODO')
    def test_generate_thumb(self):
        result = genreate_thumb(util.path('resource', 'gray.jpg'), 100, 75)
        self.addCleanup(os.unlink, result)
        result = genreate_thumb(util.path('resource', 'gray.png'), 100, 75)
        self.addCleanup(os.unlink, result)


if __name__ == '__main__':
    main()
