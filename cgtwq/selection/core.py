# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


# _OS = {'windows': 'win', 'linux': 'linux', 'darwin': 'mac'}.get(
#     __import__('platform').system().lower())  # Server defined os string.

# Above `os` string seems to be cgtw internal usage,
# brings unexpected result in production.
_OS = 'win'

TYPE_CHECKING = False
if TYPE_CHECKING:
    import cgtwq


class SelectionAttachment(object):
    """Attachment feature for selection.  """
    # pylint: disable=too-few-public-methods

    def __init__(self, selection):
        # type: (cgtwq.Selection) -> None
        from .selection import Selection
        assert isinstance(selection, Selection)
        self.select = selection
        self.call = self.select.call
