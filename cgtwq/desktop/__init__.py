# -*- coding=UTF-8 -*-
# pyright: strict, reportTypeCommentUsage=none

from __future__ import absolute_import, division, print_function, unicode_literals


from ._client_impl import new_client, current_client

TYPE_CHECKING = False
if TYPE_CHECKING:
    from ._client import Client
    from ._plugin_service import PluginService
    from ._view_service import ViewService

    __all__ = ["new_client", "current_client", "Client", "PluginService", "ViewService"]
