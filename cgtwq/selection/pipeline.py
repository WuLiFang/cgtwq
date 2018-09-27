# -*- coding=UTF-8 -*-
"""Database on cgtw server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import core
from ..core import ControllerGetterMixin
from ..filter import Field
from ..model import PipelineInfo


class SelectionPipeline(core.SelectionAttachment, ControllerGetterMixin):
    """Pipeline feature for selection.  """
    # pylint: disable=too-few-public-methods

    def all(self):
        """Get all selection related pipelines.

        Args:
            *filters (FilterList, Filter): Filters for server.

        Returns:
            tuple[PipelineInfo]
        """

        # XXX: Should use a dedicated API.
        select = self.select
        return select.module.database.pipeline.filter(
            Field('entity_name').in_(select.distinct(key='pipeline'))
        )

    def one(self):
        """Get pipeline information for the selection.

        Raises:
            ValueError: Multiple related pipeline.

        Returns:
            PipelineInfo

        """

        ret = self.all()
        if len(ret) != 1:
            raise ValueError('Multiple related pipeline.')

        ret = ret[0]
        assert isinstance(ret, PipelineInfo), type(ret)
        return ret
