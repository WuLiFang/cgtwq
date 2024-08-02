# -*- coding=UTF-8 -*-
# pyright: strict

from __future__ import annotations

from typing import Protocol, Text

from ._image import Image

class ImageService(Protocol):
    def upload(
        self,
        database: Text,
        filename: Text,
        /,
    ) -> Image: ...
