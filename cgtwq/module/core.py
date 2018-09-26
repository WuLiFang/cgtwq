# -*- coding=UTF-8 -*-
"""Database module.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


class ModuleAttachment(object):
    """Attachment feature for selection.  """
    # pylint: disable=too-few-public-methods

    def __init__(self, module):
        from .module import Module
        assert isinstance(module, Module)
        self.module = module
        self.call = self.module.call
