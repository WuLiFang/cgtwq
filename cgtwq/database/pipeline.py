# -*- coding=UTF-8 -*-
"""Database on cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..core import ControllerGetterMixin
from ..filter import Field, FilterList
from ..model import PipelineInfo
from . import core

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Tuple, Union

    import cgtwq


class DatabasePipeline(core.DatabaseAttachment, ControllerGetterMixin):
    """Pipeline feature for database.  """
    # pylint: disable=too-few-public-methods

    def filter(self, *args):
        # type: (Union[FilterList, cgtwq.Filter]) -> Tuple[PipelineInfo, ...]
        r"""Filter pipeline in the database.

        Args:
            \*filters (FilterList, Filter): Filters for server.

        Returns:
            tuple[PipelineInfo]
        """

        filters = (FilterList.from_arbitrary_args(*args)
                   or FilterList(Field('entity_name').has('%')))

        return self._filter_model(
            "c_pipeline", "get_with_filter",
            PipelineInfo, filters)
