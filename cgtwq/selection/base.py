# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from six import text_type

from ..filter import Field
from ..resultset import ResultSet

# _OS = {'windows': 'win', 'linux': 'linux', 'darwin': 'mac'}.get(
#     __import__('platform').system().lower())  # Server defined os string.

# Above `os` string seems to be cgtw internal usage,
# brings unexpected result in production.
_OS = 'win'


class BaseSelection(tuple):
    """Selection on a database module.   """

    _token = None

    def __new__(cls, module, *id_list):
        # pylint: disable=unused-argument
        assert all(isinstance(i, text_type) for i in id_list), id_list
        return super(BaseSelection, cls).__new__(cls, id_list)

    def __init__(self, module, *id_list):
        """
        Args:
            module (Module): Related module.
            *id_list: Selected id.
        """
        # pylint: disable=unused-argument

        super(BaseSelection, self).__init__()
        from ..module import Module
        assert isinstance(module, Module)
        self.module = module

    def __getitem__(self, name):
        if isinstance(name, int):
            return super(BaseSelection, self).__getitem__(name)
        return self.get_fields(name).column(name)

    def __setitem__(self, name, value):
        assert isinstance(name, (text_type, str))
        self.set_fields(**{name: value})

    @property
    def token(self):
        """User token.   """

        return self._token or self.module.token

    @token.setter
    def token(self, value):
        self._token = value

    def call(self, *args, **kwargs):
        """Call on this selection.   """

        kwargs.setdefault('token', self.token)
        return self.module.call(*args, id_array=self, **kwargs)

    def filter(self, filters):
        """Filter selection again.

        Args:
            filters (Filter,FilterList): Addtional filters.

        Returns:
            Selction: Filtered selection.
        """

        return self.module.filter((Field('id') | self) & filters)

    def get_fields(self, *fields):
        """Get field information for the selection.

        Args:
            *fields: Server defined field sign.

        Returns:
            ResultSet: Optimized tuple object contains fields data.
        """

        server_fields = [self.module.field(i) for i in fields]
        resp = self.call("c_orm", "get_in_id",
                         sign_array=server_fields,
                         order_sign_array=server_fields)
        return ResultSet(server_fields, resp.data, self.module)

    def set_fields(self, **data):
        """Set field data for the selection.

        Args:
            **data: Field name as key, Value as value.
        """

        data = {
            self.module.field(k): v for k, v in data.items()
        }
        resp = self.call("c_orm", "set_in_id",
                         sign_data_array=data)
        if resp.code == 0:
            raise ValueError(resp)

    def delete(self):
        """Delete the selected item on database.  """

        self.call("c_orm", "del_in_id")
