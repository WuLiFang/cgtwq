# -*- coding=UTF-8 -*-
"""CGTeamWork style message, support image.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json

import six

from . import server
from .model import ImageInfo


class Message(six.text_type):
    """CGTeamWork style message, support image.  """

    def __new__(cls, obj):
        ret = super(Message, cls).__new__(cls, obj)
        ret.images = []
        return ret

    def _check_images(self):
        if any(not isinstance(i, ImageInfo) for i in self.images):
            raise ValueError(
                'Invalid images with the message, maybe not uploaded or wrong data format.')

    def dumps(self):
        """Dump data to string in server defined format.  """

        self._check_images()
        return json.dumps({'data': self, 'image': [i._asdict() for i in self.images]})

    def upload_images(self, folder, token):
        """Upload contianed images to server. will replace items in `self.image`.  """

        for index, img in enumerate(self.images):
            self.images[index] = _upload_image(img, folder, token)

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
        ret.images = [ImageInfo(**i) for i in images]
        assert isinstance(ret, Message)
        return ret


def _upload_image(image, folder, token):
    if isinstance(image, ImageInfo):
        return image
    elif isinstance(image, dict):
        if image.get('max') and image.get('min'):
            return ImageInfo(max=image['max'], min=image['min'], path=image.get('path'))
        elif image.get('path'):
            image = image['path']
        else:
            raise TypeError(
                'ImageInfo takes dictionary that has key (max, min, path?).', image.keys())

    if not isinstance(image, (six.text_type, six.binary_type)):
        raise TypeError('Not support such data type.', type(image))

    return server.web.upload_image(image, folder, token)
