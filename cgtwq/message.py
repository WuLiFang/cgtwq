# -*- coding=UTF-8 -*-
"""CGTeamWork style message, support image.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json

import six


class Message(six.text_type):
    """CGTeamWork style message, support image.  """

    def __new__(cls, obj):
        ret = super(Message, cls).__new__(cls, obj)
        ret.images = []
        return ret

    def dumps(self):
        """Dump data to string in server defined format.  """

        return json.dumps({'data': self, 'image': self.images})

    @classmethod
    def load(cls, data):
        """Create message from data.  """

        if isinstance(data, cls):
            return data

        data = data or ''

        try:
            data = json.loads(data)
            assert isinstance(data, dict), type(data)
            text = data.get('data', '')
            images = data.get('image', data.get('images', []))
        except ValueError:
            text = data
            images = []

        ret = cls(text)
        ret.images = images
        assert isinstance(ret, Message)
        return ret
