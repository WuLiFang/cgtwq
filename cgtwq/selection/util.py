# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from six import text_type

from .base import BaseSelection
from .file import FileMixin
from .filebox import FileboxMixin
from .history import HistoryMixin
from .link import LinkMixin
from .message import MessageMixin
from .note import NoteMixin


class Selection(FileMixin, MessageMixin, NoteMixin,
                FileboxMixin, LinkMixin, HistoryMixin,
                BaseSelection):
    """Selection with all feature.  """

    def to_entry(self):
        """Convert selection to one entry.

        Raises:
            ValueError: Not exactly one selected item.

        Returns:
            Entry: Entry.
        """

        if len(self) != 1:
            raise ValueError('Need exactly one selected item.')

        return Entry(self.module, self[0])

    def to_entries(self):
        """Convert selection to entries.

        Returns:
            tuple[Entry]: Entries.
        """

        return tuple(Entry(self.module, i) for i in self)


class Entry(Selection):
    """A selection that only has one item.  """

    def __init__(self, module, id_):
        assert isinstance(id_, text_type), type(id_)
        super(Entry, self).__init__(module, id_)

    def __getitem__(self, name):
        if isinstance(name, int):
            return super(Entry, self).__getitem__(name)
        return self.get_fields(name)[0]

    def get_fields(self, *fields):
        """Get multiple fields.

        Returns:
            tuple: Result fields with exactly same order with `fields`.
        """

        ret = super(Entry, self).get_fields(*fields)
        assert len(ret) == 1, ret
        ret = ret[0]
        assert isinstance(ret, list), ret
        return tuple(ret)

    def get_image(self, field='image'):
        """Get imageinfo used on the field.

        Args:
            field (text_type): Defaults to 'image', Server defined field name,

        Raises:
            ValueError: when no image in the field.

        Returns:
            ImageInfo: Image information.
        """

        try:
            return self._to_selection().get_image(field)[0]
        except IndexError:
            raise ValueError('No image in this field.', field)

    def _to_selection(self):
        return Selection(self.module, *self)
