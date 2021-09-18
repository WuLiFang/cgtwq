# -*- coding=UTF-8 -*-
"""Helper for cgtwq query with WuLiFang style naming schema.  """
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import re

import cast_unknown as cast
import cgtwq
from deprecated import deprecated
from pathlib2_unicode import PurePath
from six import text_type

from .exceptions import DatabaseError

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Dict, Text, Any, Callable, List


LOGGER = logging.getLogger(__name__)


CACHE = {}

CACHE_KEY_PREFIX_DATABASE_MAP = "prefix_database_map"


def _get_shot(path, version_pattern=r"(.+)v(\d+)"):
    # type: (Text, Text) -> Text
    """The related shot for this footage.

    >>> _get_shot('sc_001_v20.nk')
    u'sc_001'
    >>> _get_shot('hello world')
    u'hello world'
    >>> _get_shot('sc_001_v-1.nk')
    u'sc_001_v-1'
    >>> _get_shot('sc001V1.jpg')
    u'sc001'
    >>> _get_shot('sc001V1_no_bg.jpg')
    u'sc001'
    >>> _get_shot('suv2005_v2_m.jpg')
    u'suv2005'
    """

    p = PurePath(cast.text(path))
    match = re.match(version_pattern, cast.text(p.name), flags=re.I)
    if not match:
        return cast.text(p.stem)
    shot = match.group(1)
    return shot.strip("_")


def guess_entry(select):
    # type: (cgtwq.Selection) -> cgtwq.Entry
    """Get best matched entry from select.

    Args:
        select (Selection): CGTeamWork selection.

    Returns:
        Entry: CGTeamWork entry.
    """

    current_account_id = cgtwq.current_account_id()
    data = select.get_fields("id", "account_id")
    data = {i[0]: i[1] and i[1].split(",") for i in data}
    entries = select.to_entries()

    def _by_artist(entry):
        # type: (cgtwq.Entry) -> int
        task_account_id = data[entry[0]]
        if not task_account_id:
            return 2
        if current_account_id in task_account_id:
            return 0
        return 1

    entries = sorted(entries, key=_by_artist)

    return entries[0]


def get_database_by_file(filename):
    # type: (Text) -> Text
    """Get database name from filename.

    Args:
        filename (str): Filename.

    Raises:
        DatabaseError: When can not determinate database from filename.

    Returns:
        str: Database name.
    """

    if CACHE_KEY_PREFIX_DATABASE_MAP not in CACHE:
        data = {}  # type: Dict[text_type, text_type]
        result_set = cgtwq.PROJECT.select_activated().get_fields(
            "code",
            "database",
            "filename_prefix",
        )
        # default to database code
        for i in result_set:
            data[i[0].lower() + "_"] = i[1]

        # read settings from `filename_prefix` field
        # not use database metadata because it will be duplicated when clone project settings.
        for i in result_set:
            for j in text_type(i[2] or "").lower().split("\n"):
                if not j:
                    continue
                data[j] = i[1]
        CACHE[CACHE_KEY_PREFIX_DATABASE_MAP] = data
    prefix_database_map = CACHE[CACHE_KEY_PREFIX_DATABASE_MAP]

    norm_filename = (text_type(filename)).lower()
    for k in prefix_database_map:
        if norm_filename.startswith(k):
            return prefix_database_map[k]

    raise DatabaseError("Can not determinate database from filename.", filename)


def get_entry_by_file(filename, pipeline, module="shot"):
    # type: (Text, Text, Text) -> cgtwq.Entry
    """Get entry from filename and pipeline

    Args:
        filename (str): Filename to determinate shot.
        pipeline (str): Server defined pipline name.
        module (str): Defaults to `shot`, Server defined module name.

    Returns:
        cgtwq.Entry: Entry
    """

    shot = _get_shot(filename)
    database = cgtwq.Database(get_database_by_file(filename))
    select = database.module(module).filter(
        (cgtwq.Field("pipeline") == pipeline) & (cgtwq.Field("shot.shot") == shot)
    )
    try:
        entry = select.to_entry()
    except ValueError:
        LOGGER.warning("Duplicated task: %s", shot)
        entry = guess_entry(select)

    return entry


@deprecated(version="3.0.0", reason="Use other functions instead.")
class CGTWQHelper(object):  # TODO: remove this at next major version.
    """DEPRECATED: Helper class for cgtwq query.

    Attributes:
        prefix_filters: Function list that filter project code to prefix.
    """

    cache = {}
    prefix_filters = []  # type: List[Callable[[Text], Text]]

    @classmethod
    def project_data(cls):
        # type: () -> Any
        """Cached project data."""

        if "project_data" not in cls.cache:
            cls.cache["project_data"] = cgtwq.PROJECT.select_activated().get_fields(
                "code", "database"
            )
        return cls.cache["project_data"]

    @classmethod
    def get_prefix(cls, code):
        # type: (Text) -> Text
        """Use filters to get prefix from project code."""

        ret = code
        for i in cls.prefix_filters:
            ret = i(ret)
        return ret

    @classmethod
    def get_database(cls, filename):
        # type: (Text) -> Text
        """Get database name from filename.

        Args:
            filename (str): Filename.

        Raises:
            DatabaseError: When can not determinate database from filename.

        Returns:
            str: Database name.
        """

        prefix_database_map = {}
        for i in cls.project_data():
            code, database = i
            prefix = cls.get_prefix(code)
            prefix_database_map[prefix] = database

        prefix = text_type(filename).split("_")[0]
        if prefix in prefix_database_map:
            return prefix_database_map[prefix]
        for k in prefix_database_map:
            if (text_type(filename)).startswith(k):
                return prefix_database_map[k]

        raise DatabaseError("Can not determinate database from filename.", filename)

    @classmethod
    def get_entry(cls, filename, pipeline, module="shot"):
        # type: (Text, Text, Text) -> cgtwq.Entry
        """Get entry from filename and pipeline

        Args:
            filename (str): Filename to determinate shot.
            pipeline (str): Server defined pipline name.
            module (str): Defaults to `shot`, Server defined module name.

        Returns:
            cgtwq.Entry: Entry
        """

        key = (filename, pipeline)
        if key in cls.cache:
            return cls.cache[key]

        shot = _get_shot(filename)
        database = cgtwq.Database(cls.get_database(filename))
        select = database.module(module).filter(
            (cgtwq.Field("pipeline") == pipeline) & (cgtwq.Field("shot.shot") == shot)
        )
        try:
            entry = select.to_entry()
        except ValueError:
            LOGGER.warning("Duplicated task: %s", shot)
            entry = CGTWQHelper.guess_entry(select)

        cls.cache[key] = entry

        return entry

    @staticmethod
    def guess_entry(select):
        # type: (cgtwq.Selection) -> cgtwq.Entry
        """DEPRECATED: use top level `guess_entry` instead.
        Get best matched entry from select.

        Args:
            select (Selection): CGTeamWork selection.

        Returns:
            Entry: CGTeamWork entry.
        """

        return guess_entry(select)
