# -*- coding=UTF-8 -*-
"""Data models.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
from collections import namedtuple


class FileBoxCategoryInfo(namedtuple('FileBoxInfo', ('id', 'pipeline_id', 'title'))):
    """Filebox catagory information.  """

    fields = ('#id', '#pipeline_id', 'title')


class PipelineInfo(namedtuple('PipelineInfo',
                              ('id', 'name', 'module',
                               'module_type', "description"))):
    """Pipeline information.  """
    fields = ("#id", "entity_name", "module", "module_type", "description")


class NoteInfo(namedtuple('NoteInfo',
                          ('id', 'task_id', 'account_id',
                           'html', 'time', 'account_name',
                           'module'))):
    """Note informatiom.  """

    fields = ('#id', '#task_id', '#from_account_id',
              'text', 'time', 'create_by',
              'module')


class HistoryInfo(
        namedtuple(
            'HistoryInfo',
            ('id', 'task_id', 'account_id',
             'step', 'status', 'file',
             'text', 'create_by', 'time')
        )):
    """History information.   """

    fields = ('#id', '#task_id', '#account_id',
              'step', 'status', 'file',
              'text', 'create_by', 'time')

    def __new__(cls, *args, **kwargs):
        from .message import Message
        raw = super(HistoryInfo, cls).__new__(cls, *args, **kwargs)
        data = raw._asdict()
        data['text'] = Message.load(raw.text)
        return super(HistoryInfo, cls).__new__(cls, **data)


class FileBoxInfo(namedtuple(
        'FileBoxInfo',
        ('id', 'path', 'classify',
         'title', 'sign', 'color', 'rule',
         'rule_view', 'show_type', 'server', 'drag_in',
         'is_submit', 'is_move_old_to_history',
         'is_move_same_to_history', 'is_in_history_add_version',
         'is_in_history_add_datetime', 'is_cover_disable',
         'is_msg_to_first_qc'))):
    """Filebox information.   """
    def __new__(cls, *args, **kwargs):
        kwargs['id'] = kwargs.pop('#id')
        return super(FileBoxInfo, cls).__new__(cls, *args, **kwargs)
    fileds = ('#id', 'path', 'classify',
              'title', 'sign', 'color', 'rule',
              'rule_view', 'show_type', 'server', 'drag_in',
              'is_submit', 'is_move_old_to_history',
              'is_move_same_to_history', 'is_in_history_add_version',
              'is_in_history_add_datetime', 'is_cover_disable',
              'is_msg_to_first_qc')


class ImageInfo(namedtuple('ImageInfo', ('max', 'min', 'path'))):
    """Image infromation.  """

    def __new__(cls, max, min, path=None):
        # pylint: disable=redefined-builtin
        return super(ImageInfo, cls).__new__(cls, max, min, path)

    def __getitem__(self, index):
        # TODO: remove at next major version.
        if index in self._fields:
            LOGGER.warning('Use ImageInfo.%s to get value from namedtuple, '
                           'this compatibility support will '
                           'deprecate at next major version.', index)
            return getattr(self, index)
        return super(ImageInfo, self).__getitem__(index)


LOGGER = logging.getLogger(__name__)


class FieldInfo(
        namedtuple(
            'FieldInfo',
            ('id', 'module', 'sign',
             'type', 'label', 'is_sys',
             'see_permission', 'edit_permission',
             'is_required', 'is_lock', 'is_show_edit',
             'sort_id')
        )):
    """Field information.   """

    fields = ('#id', 'module', 'sign',
              'type', 'field_str', 'is_sys',
              'see_permission', 'edit_permission',
              'is_required', 'lock', 'edit_is_show',
              'sort_id')

    def __new__(cls, *args, **kwargs):
        raw = super(FieldInfo, cls).__new__(cls, *args, **kwargs)
        new_kwargs = raw._asdict()
        _format_yn_str_in_dict(new_kwargs)
        return super(FieldInfo, cls).__new__(cls, **new_kwargs)


def _format_yn_str_in_dict(dict_):
    for k, v in dict_.items():
        if k.startswith('is_'):
            dict_[k] = _format_yn_str(v)


def _format_yn_str(text):
    try:
        return {'Y': True,
                'N': False,
                '': None,
                None: None}[text]
    except KeyError:
        raise ValueError(text)


StatusInfo = namedtuple('StatusInfo', ('status', 'color'))


class ModuleInfo(namedtuple('ModuleInfo', ('label', 'name', 'type'))):
    """Module information.   """

    fields = ('module_str', 'module', 'type')


AccountInfo = namedtuple('AccountInfo',
                         ('account', 'account_id', 'image',
                          'update_time', 'file_key', 'token',
                          'client_type', 'remote_ip', 'name',
                          'password_comlexity'))

FlowInfo = namedtuple('FlowInfo',
                      ('flow_id', 'pipeline_id'))

PluginData = namedtuple(
    'PulginData',
    ('plugin_id',
     'filebox_id',
     'database',
     'module',
     'module_type',
     'id_list',
     'folder',
     'file_path_list',
     'argv',
     'retake_pipeline_id_list')
)
