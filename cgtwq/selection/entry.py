# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from six import text_type

from ..model import ImageInfo
from .selection import Selection


class Entry(Selection):
    """A selection that only has one item.  """

    def __init__(self, module, id_):
        assert isinstance(id_, text_type), type(id_)
        super(Entry, self).__init__(module, id_)

    def __getitem__(self, name):
        if isinstance(name, int):
            return super(Entry, self).__getitem__(name)
        return self.get_fields(name)[0]

    def get_fields(self, *fields, **kwargs):
        """Get multiple fields.

        Returns:
            tuple: Result fields with exactly same order with `fields`.
        """

        ret = super(Entry, self).get_fields(*fields, **kwargs)
        assert len(ret) == 1, ret
        ret = ret[0]
        assert isinstance(ret, list), ret
        return tuple(ret)

    def related(self, *filters):
        """Select related entries.

        Args:
            *filters: Pipeline filters.

        Returns:
            Selection
        """

        pipelines = self.module.database.pipeline.filter(*filters)
        resp = self.call('c_note', 'get_task_id_array',
                         task_id=self[0],
                         pipeline_id_array=[i.id for i in pipelines])
        return self.module.select(*resp)

    # Deprecated methods.
    # TODO: Remove at next major version.

    def _get_image(self, field='image'):
        """Get imageinfo used on the field.

        Args:
            field (text_type): Defaults to 'image', Server defined field name,

        Raises:
            ValueError: when no image in the field.

        Returns:
            ImageInfo: Image information.
        """

        try:
            ret = super(Entry, self).get_image(field)[0]
            assert isinstance(ret, ImageInfo), type(ret)
            return ret
        except IndexError:
            raise ValueError('No image in this field.', field)
