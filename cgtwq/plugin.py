# -*- coding=UTF-8 -*-
"""Handle CGTeamWork plugin data.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
from functools import partial

from . import server


class PlugIn(object):
    def __init__(self, id_):
        self.id = id_
        self.call = partial(server.call, 'c_plugin', id=self.id)

    def get_fields(self, fields):
        return self.call('get_one_with_id', id=self.id, field_array=fields)

    def get_argvs(self):
        return self.get_fields(['argvs'])

    def set_argvs(self, **data):
        self.call('set_one_with_id',
                  id=self.id,
                  field_data_array={'argv': json.dumps(data)})

    @classmethod
    def filter(cls, filters):
        resp = server.call("c_plugin", "get_with_filter",
                           field_array=['#id'], filter_array=filters)

        return tuple(cls(i) for i in resp.data)

    @classmethod
    def type(cls, name):
        resp = server.call("c_plugin", "get_with_type",
                           field_array=['#id'], type=name)

        return tuple(cls(i) for i in resp.data)
