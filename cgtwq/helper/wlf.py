# -*- coding=UTF-8 -*-
"""Helper for cgtwq query with WuLiFang style naming schema.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

from six import text_type

import cgtwq
from wlf.path import PurePath

from .exceptions import DatabaseError

LOGGER = logging.getLogger(__name__)


class CGTWQHelper(object):
    """Helper class for cgtwq query.

    Attributes:
        prefix_filters: Function list that filter project code to prefix.
    """
    cache = {}
    prefix_filters = []

    @classmethod
    def project_data(cls):
        """Cached project data.  """

        if 'project_data' not in cls.cache:
            cls.cache['project_data'] = cgtwq.PROJECT.all(
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

        for i in cls.project_data():
            code, database = i
            prefix = cls.get_prefix(code)
            if text_type(filename).startswith(prefix):
                return database
        raise DatabaseError(
            'Can not determinate database from filename.', filename)

    @classmethod
    def get_entry(cls, filename, pipeline):
        """Get entry from filename and pipeline

        Args:
            filename (str): Filename to determinate shot.
            pipeline (str): Server defined pipline name.

        Returns:
            cgtwq.Entry: Entry
        """

        key = (filename, pipeline)
        if key not in cls.cache:
            database = cls.get_database(filename)
            shot = PurePath(filename).shot
            module = cgtwq.Database(database)['shot_task']
            select = module.filter(
                (cgtwq.Field('pipeline') == pipeline)
                & (cgtwq.Field('shot.shot') == shot)
            )
            try:
                entry = select.to_entry()
            except ValueError:
                LOGGER.warning('Duplicated task: %s', shot)

                current_account_id = cgtwq.current_account_id()
                data = select.get_fields('id', 'account_id')
                data = {i[0]: i[1].split(',') for i in data}

                def _by_artist(id_):
                    task_account_id = data[id_]
                    if not task_account_id:
                        return 2
                    if current_account_id in task_account_id:
                        return 0
                    return 1
                entries = select.to_entries()
                entry = sorted(entries, key=_by_artist)[0]

            cls.cache[key] = entry

        return cls.cache[key]
