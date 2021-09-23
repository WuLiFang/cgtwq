# -*- coding=UTF-8 -*-
"""Database on cgtw server.  """
from __future__ import absolute_import, division, print_function, unicode_literals

from ..filter import Field, FilterList
from ..model import FileBoxMeta, PipelineInfo
from . import core

from .. import compat
from deprecated import deprecated

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text, Tuple, Union
    import cgtwq
    import cgtwq.model


class DatabaseFilebox(core.DatabaseAttachment):
    """Filebox feature for database."""

    def _filter_v5_2(self, *args):
        # type: (Union[FilterList, cgtwq.Filter]) -> Tuple[FileBoxMeta, ...]

        filters = FilterList.from_arbitrary_args(*args) or FilterList(
            Field("#id").has("%")
        )
        resp = self.call(
            "c_file",
            "get_with_filter",
            field_array=FileBoxMeta.fields_v5_2,
            filter_array=filters,
        )
        return tuple(FileBoxMeta(*i) for i in resp)  # type: ignore https://github.com/microsoft/pyright/issues/2325

    def _filter_v6_1(self, *args):
        # type: (Union[FilterList, cgtwq.Filter]) -> Tuple[FileBoxMeta, ...]

        raise NotImplementedError("this api not available in cgteamwork 6.1")

    @deprecated(
        version="3.2.3",
        reason="not avaliable in cgteamwork 6.1, use list_by_pipeline instead",
    )
    def filter(self, *args):
        # type: (Union[FilterList, cgtwq.Filter]) -> Tuple[FileBoxMeta, ...]
        r"""Filter fileboxes metadata in the database.

        Args:
            \*filters (FilterList, Filter): Filters for server.

        Returns:
            tuple[FileBoxMeta]: namedtuple for ('id', 'pipeline_id', 'title')
        """

        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._filter_v5_2(*args)
        return self._filter_v6_1(*args)

    def _list_by_pipeline_v5_2(self, *pipelines):
        # type: (PipelineInfo) -> Tuple[FileBoxMeta, ...]

        filters = FilterList(Field("#pipeline_id").in_([i.id for i in pipelines]))
        resp = self.call(
            "c_file",
            "get_with_filter",
            field_array=FileBoxMeta.fields_v5_2,
            filter_array=filters,
        )
        return tuple(FileBoxMeta(*i) for i in resp)  # type: ignore https://github.com/microsoft/pyright/issues/2325

    def _list_by_pipeline_v6_1(self, *pipelines):
        # type: (PipelineInfo) -> Tuple[FileBoxMeta, ...]
        class local:
            ret = ()
            ids = []

        if not pipelines:
            return local.ret

        pipelines = tuple(sorted(pipelines, key=lambda x: (x.module, x.module_type)))
        module = pipelines[0].module
        module_type = pipelines[0].module_type

        def _flush():
            if not local.ids:
                return
            resp = self.call(
                "c_filebox",
                "get_with_pipeline_id",
                module=module,
                module_type=module_type,
                field_array=FileBoxMeta.fields_v6_1,
                pipeline_id_array=local.ids,
            )
            local.ret += tuple(FileBoxMeta(*i) for i in resp)  # type: ignore https://github.com/microsoft/pyright/issues/2325
            local.ids = []

        for p in pipelines:
            if (p.module, p.module_type) != (module, module_type):
                _flush()
            module, module_type = p.module, p.module_type
            local.ids.append(p.id)
        _flush()

        return local.ret

    def list_by_pipeline(self, *pipelines):
        # type: (PipelineInfo) -> Tuple[FileBoxMeta, ...]
        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._list_by_pipeline_v5_2(*pipelines)
        return self._list_by_pipeline_v6_1(*pipelines)

    def _get_v5_2(self, id_):
        # type: (Text) -> FileBoxMeta
        resp = self.call(
            "c_file", "get_one_with_id", id=id_, field_array=FileBoxMeta.fields_v5_2
        )
        return FileBoxMeta(*resp)  # type: ignore https://github.com/microsoft/pyright/issues/2325

    def _get_v6_1(self, id_):
        # type: (Text) -> FileBoxMeta
        raise NotImplementedError("not avaliable in cgteamwork 6.1")

    @deprecated(
        version="3.2.3",
        reason="not available in cgteamwork 6.1",
    )
    def get(self, id_):
        # type: (Text) -> FileBoxMeta
        r"""Get filebox metadata from the database.

        Args:
            id_ (str): Filebox id.

        Returns:
            FileboxMeta
        """

        fields = FileBoxMeta.fields_v6_1
        if compat.api_level() == compat.API_LEVEL_5_2:
            return self._get_v5_2(id_)
        return self._get_v6_1(id_)

    from_id = deprecated(version="3.0.0", reason="use get instead")(get)
