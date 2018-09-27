# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import uuid

import six

from wlf.codectools import get_encoded as e

from .. import account, exceptions
from ..filter import Field
from ..message import Message
from .core import SelectionAttachment


class SelectionFlow(SelectionAttachment):
    """Flow operation on selection.  """

    def update(self, field, status, message='', images=()):
        """Update flow status.  """
        # TODO: refactor arguments at next major version.

        select = self.select
        message = Message.load(message)
        message.images += images
        field = Field(field).in_namespace(
            self.select.module.default_field_namespace)

        try:
            self.call('c_work_flow', 'python_update_flow',
                      field_sign=field,
                      status=status,
                      text=message.dumps(),
                      task_id=select[0])
        except ValueError as ex:
            if (ex.args
                    and ex.args[0] == ('work_flow::python_update_flow, '
                                       'no permission to qc')):
                raise exceptions.PermissionError
            raise

    def submit(self, filenames=(), message="", account_id=None):
        """Submit file to task, then change status to `Check`.

        Args:
            pathnames (tuple, optional): Defaults to (). Server pathnames.
            filenames (tuple, optional): Defaults to (). Local filenames.
            message (Message, optional): Defaults to "". Submit note(and images).
        """

        select = self.select
        message = Message.load(message)
        account_id = account_id or account.get_account_id(select.token)

        # Create path data.
        path_data = {'path': [], 'file_path': []}
        for i in filenames:
            path_data['path' if os.path.isdir(e(i)) else 'file_path'].append(i)

        select.call(
            "c_work_flow", "submit",
            task_id=select[0],
            account_id=account_id,
            version_id=self.create_version(filenames),
            submit_file_path_array=path_data,
            text=message.dumps())

    def create_version(self, filenames, sign='Api Submit', version_id=None):
        """Create new task version.

        Args:
            filenames (list): Filename list.
            sign (str, optional): Defaults to 'Api Submit'. Server version sign.
            version_id (str, optional): Defaults to None. Wanted version id.

        Returns:
            str: Created version id.
        """

        select = self.select
        version_id = version_id or uuid.uuid4().hex
        select.call(
            'c_version', 'create',
            field_data_array={
                "#link_id": select[0],
                "version": "",
                "filename": [os.path.basename(i) for i in filenames],
                "local_path": filenames,
                "web_path": [],
                "sign": sign,
                "image": "",
                "from_version": "",
                "is_upload_web": "N",
                "#id": version_id,
            }
        )
        return version_id

    def assign(self, accounts, start='', end=''):
        """Assgin tasks.

        Args:
            account (list): Account id list.
            start (str, optional): Defaults to ''. Task start date.
            end (str, optional): Defaults to ''. Task end date.
        """

        if isinstance(accounts, six.text_type):
            accounts = [accounts]
        select = self.select
        select.call('c_work_flow', 'assign_to',
                    assign_account_id=','.join(accounts),
                    start_date=start,
                    end_date=end,
                    task_id_array=select)

    def has_field_permission(self, field):
        """Return if current user has permission to edit the field.  """

        field = Field(field).in_namespace(
            self.select.module.default_field_namespace)
        resp = self.call(
            'c_work_flow', 'is_status_field_has_permission',
            field_sign=field,
            task_id_array=self.select
        )
        return resp

    def close(self, field, message='', images=()):
        """Shorthand method to set take status to `Close`.  """

        return self.update(field, 'Close', message, images)

    def approve(self, field, message='', images=()):
        """Shorthand method to set take status to `Approve`.  """

        return self.update(field, 'Approve', message, images)

    def retake(self, field, message='', images=()):
        """Shorthand method to set take status to `Retake`.  """

        return self.update(field, 'Retake', message, images)
