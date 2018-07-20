# -*- coding=UTF-8 -*-
"""Common methods.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .filter import FilterList


class ControllerGetterMixin(object):
    """Mixin for controller getter.  """

    def _get_model(self, controller, method, model, filters):
        """Get infomation from controller with data model.

        Args:
            object (obj): Object to mixin.
            controller (str): Server defined controller name.
            method (str): Server defined method name.
            filters (FilterList): Filters.
            model (namedtuple): Data model.

        Returns:
            tuple[model]: Result
        """

        fields = getattr(model, 'fields', model._fields)
        resp = self.call(
            controller, method,
            field_array=fields,
            filter_array=FilterList(filters))
        return tuple(model(*i) for i in resp)
