# -*- coding=UTF-8 -*-
"""Helper for cgtwq query with WuLiFang style naming schema.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import typing

from six import text_type

import cgtwq
from wlf.path import PurePath

from .exceptions import DatabaseError

LOGGER = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    pass


CACHE = {}

CACHE_KEY_PREFIX_DATABASE_MAP = "prefix_database_map"


def guess_entry(select):
    """Get best matched entry from select.

    Args:
        select (Selection): CGTeamWork selection.

    Returns:
        Entry: CGTeamWork entry.
    """

    current_account_id = cgtwq.current_account_id()
    data = select.get_fields('id', 'account_id')
    data = {i[0]: i[1] and i[1].split(',') for i in data}
    entries = select.to_entries()

    def _by_artist(entry):
        task_account_id = data[entry[0]]
        if not task_account_id:
            return 2
        if current_account_id in task_account_id:
            return 0
        return 1

    entries = sorted(entries, key=_by_artist)

    return entries[0]


def get_database_by_file(filename):
    """Get database name from filename.

    Args:
        filename (str): Filename.

    Raises:
        DatabaseError: When can not determinate database from filename.

    Returns:
        str: Database name.
    """

    if CACHE_KEY_PREFIX_DATABASE_MAP not in CACHE:
        data = {}  # type: typing.Dict[text_type, text_type]
        select = cgtwq.PROJECT.select_activated().get_fields(
            'code',
            'database',
            'last_update_time',
        )
        select.sort(key=lambda x: x[2])
        for i in reversed(select):
            database = cgtwq.Database(i[1])
            data[i[0].lower() + "_"] = database.name
            for j in text_type(database.metadata["filename_prefix"] or "").lower().split(","):
                if not j:
                    continue
                data[j] = database.name
        CACHE[CACHE_KEY_PREFIX_DATABASE_MAP] = data
    prefix_database_map = CACHE[CACHE_KEY_PREFIX_DATABASE_MAP]

    norm_filename = (text_type(filename)).lower()
    for k in prefix_database_map:
        if norm_filename.startswith(k):
            return prefix_database_map[k]

    raise DatabaseError(
        'Can not determinate database from filename.', filename)


def get_entry_by_file(filename, pipeline, module='shot'):
    # type: (text_type, text_type, typing.Optional[text_type]) -> cgtwq.Entry
    """Get entry from filename and pipeline

    Args:
        filename (str): Filename to determinate shot.
        pipeline (str): Server defined pipline name.
        module (str): Defaults to `shot`, Server defined module name.

    Returns:
        cgtwq.Entry: Entry
    """

    shot = PurePath(filename).shot
    database = cgtwq.Database(get_database_by_file(filename))
    select = database.module(module).filter(
        (cgtwq.Field('pipeline') == pipeline)
        & (cgtwq.Field('shot.shot') == shot))
    try:
        entry = select.to_entry()
    except ValueError:
        LOGGER.warning('Duplicated task: %s', shot)
        entry = guess_entry(select)

    return entry


class CGTWQHelper(object):  # TODO: remove this at next major version.
    """DEPRECATED: Helper class for cgtwq query.

    Attributes:
        prefix_filters: Function list that filter project code to prefix.
    """
    cache = {}
    prefix_filters = []

    @classmethod
    def project_data(cls):
        """Cached project data.  """

        if 'project_data' not in cls.cache:
            cls.cache['project_data'] = cgtwq.PROJECT.select_activated(
            ).get_fields('code', 'database')
        return cls.cache['project_data']

    @classmethod
    def get_prefix(cls, code):
        """Use filters to get prefix from project code.  """

        ret = code
        for i in cls.prefix_filters:
            ret = i(ret)
        return ret

    @classmethod
    def get_database(cls, filename):
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

        prefix = text_type(filename).split('_')[0]
        if prefix in prefix_database_map:
            return prefix_database_map[prefix]
        for k in prefix_database_map:
            if (text_type(filename)).startswith(k):
                return prefix_database_map[k]

        raise DatabaseError(
            'Can not determinate database from filename.', filename)

    @classmethod
    def get_entry(cls, filename, pipeline, module='shot'):
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

        shot = PurePath(filename).shot
        database = cgtwq.Database(cls.get_database(filename))
        select = database.module(module).filter(
            (cgtwq.Field('pipeline') == pipeline)
            & (cgtwq.Field('shot.shot') == shot))
        try:
            entry = select.to_entry()
        except ValueError:
            LOGGER.warning('Duplicated task: %s', shot)
            entry = CGTWQHelper.guess_entry(select)

        cls.cache[key] = entry

        return entry

    @staticmethod
    def guess_entry(select):
        """DEPRECATED: use top level `guess_entry` instead.
        Get best matched entry from select.

        Args:
            select (Selection): CGTeamWork selection.

        Returns:
            Entry: CGTeamWork entry.
        """

        return guess_entry(select)
