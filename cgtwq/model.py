# -*- coding=UTF-8 -*-
"""Data models.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from collections import namedtuple

# Filebox
FIELDS_FILEBOX = ('#id', '#pipeline_id', 'title')
FileBoxInfo = namedtuple('FileBoxInfo', ('id', 'pipeline_id', 'title'))
FileBoxDetail = namedtuple(
    'FileBoxDetail',
    ('path',
     'classify', 'title',
     'sign', 'color', 'rule', 'rule_view',
     'is_submit', 'is_move_old_to_history',
     'is_move_same_to_history', 'is_in_history_add_version',
     'is_in_history_add_datetime', 'is_cover_disable',
     'is_msg_to_first_qc')
)

# Pipeline
FIELDS_PIPELINE = ('#id', 'name', 'module')
PipelineInfo = namedtuple('PipelineInfo', ('id', 'name', 'module'))

# Image
ImageInfo = namedtuple('ImageInfo', ('max', 'min', 'path'))

# Note
FIELDS_NOTE = ('#id', '#task_id', '#from_account_id',
               'text', 'time', 'create_by',
               'module')
NoteInfo = namedtuple('NoteInfo',
                      ('id', 'task_id', 'account_id',
                       'html', 'time', 'account_name',
                       'module'))
# History
FIELDS_HISTORY = ('#id', '#task_id', '#account_id',
                  'step', 'status', 'file',
                  'text', 'create_by', 'time')
HistoryInfo = namedtuple('HistoryInfo',
                         ('id', 'task_id', 'account_id',
                          'step', 'status', 'file',
                          'text', 'create_by', 'time'))
