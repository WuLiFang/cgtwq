# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .. import exceptions
from .base import SelectionAttachment


class SelectionFlow(SelectionAttachment):
    """Flow operation on selection.  """

    def update(self, field, status, message=''):
        """Update flow status.  """

        select = self.select
        try:
            self.call('c_work_flow', 'python_update_flow',
                      field_sign=select.module.field(field),
                      status=status,
                      text=message,
                      task_id=select[0])
        except ValueError as ex:
            if (ex.args
                    and ex.args[0] == ('work_flow::python_update_flow, '
                                       'no permission to qc')):
                raise exceptions.PermissionError
            raise

    def has_field_permission(self, field):
        """Return if current user has permission to edit the field.  """

        field = self.select.module.field(field)
        resp = self.call(
            'c_work_flow', 'is_status_field_has_permission',
            field_sign=field,
            task_id_array=self.select
        )
        return resp

    def close(self, field, message=''):
        """Shorthand method to set take status to `Close`.  """

        return self.update(field, 'Close', message)

    def approve(self, field, message=''):
        """Shorthand method to set take status to `Approve`.  """

        return self.update(field, 'Approve', message)

    def retake(self, field, message=''):
        """Shorthand method to set take status to `Retake`.  """

        return self.update(field, 'Retake', message)
