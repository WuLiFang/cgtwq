# -*- coding=UTF-8 -*-
"""Test module `cgtwq.server` with a mocked environment."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import uuid
import six
from cgtwq import server


def test_file_operation(monkeypatch):
    def _mocked_post(*args, **kwargs):
        assert args == expected_post_arg[0]
        assert kwargs == expected_post_arg[1]
        return post_return_value

    monkeypatch.setattr(server.file, 'post', _mocked_post)

    dummy_data = six.text_type(uuid.uuid4())
    pathname = '/test_pathname-' + dummy_data
    token = 'token-' + dummy_data

    expected_post_arg = (('/file.php',),
                         {'data': {'action': 'file_exists', 'server_path': pathname},
                          'token': token})
    post_return_value = True
    assert server.exists(pathname, token)

    expected_post_arg[1]['data']['action'] = 'create_dir'
    assert server.mkdir(pathname, token)

    expected_post_arg[1]['data']['action'] = 'is_dir'
    assert server.isdir(pathname, token)

    expected_post_arg[1]['data']['action'] = 'delete'
    assert server.delete(pathname, token)

    expected_post_arg[1]['data']['action'] = 'list_dir'
    post_return_value = {'dir': [], 'file': []}
    result = server.listdir(pathname, token)
    assert result._asdict() == post_return_value
    assert result.file == []

    expected_post_arg[1]['data']['action'] = 'file_info'
    post_return_value = {'file_md5': 'md5',
                         'file_size': 'size', 'server_path': pathname}
    result = server.stat(pathname, token)
    assert result._asdict() == post_return_value

    dst = pathname + '-dst'
    expected_post_arg[1]['data'] = {
        'action': 'rename', 'old_path': pathname, 'new_path': dst}
    assert server.rename(pathname, dst, token)


def test_upload(monkeypatch, tmpdir):
    calls = []
    return_value = None

    def _mocked_post(*args, **kwargs):
        args_e, kwargs_e, return_value = calls.pop(0)

        assert args == args_e
        assert kwargs == kwargs_e
        return return_value

    def _add_call(*args, **kwargs):
        calls.append((args, kwargs, return_value))

    monkeypatch.setattr(server.file, 'post', _mocked_post)

    dummy_data = six.text_type(uuid.uuid4())
    pathname = '/test_pathname-' + dummy_data
    token = 'token-' + dummy_data

    path = tmpdir.join('testfile')
    path.write(dummy_data)
    file_md5 = path.computehash()

    return_value = {'file_pos': 0, 'is_exist': False}
    _add_call('/file.php', {'action': 'pre_upload',
                            'file_md5': file_md5,
                            'upload_des_path': pathname},
              ip=server.setting.SERVER_IP, token=token)
    _add_call('/upload_file', {'is_backup_to_history': 'Y',
                               'no_continue_upload': 'N',
                               'read_pos': 0,
                               'file_size': path.size(),
                               'file_md5': file_md5,
                               'upload_des_path': pathname},
              ip=server.setting.SERVER_IP, token=token,
              files={'files': dummy_data.encode('utf-8')})
    server.upload(six.text_type(path), pathname, token)


def test_download(monkeypatch, tmpdir):
    calls = []
    return_value = None

    def _mocked_func(*args, **kwargs):
        args_e, kwargs_e, return_value = calls.pop(0)

        assert args == args_e
        assert kwargs == kwargs_e
        return return_value

    def _add_call(*args, **kwargs):
        calls.append((args, kwargs, return_value))

    monkeypatch.setattr(server.file, 'get', _mocked_func)
    monkeypatch.setattr(server.file, 'post', _mocked_func)

    dummy_data = six.text_type(uuid.uuid4())
    pathname = '/test_pathname-' + dummy_data
    token = 'token-' + dummy_data
    path = tmpdir.join('temp')
    path.write(dummy_data)
    file_md5 = path.computehash()
    file_size = path.size()

    return_value = {'file_md5': file_md5,
                    'file_size': file_size,
                    'server_path': pathname}
    _add_call('/file.php',
              data={'action': 'file_info',
                    'server_path': pathname},
              token=token)

    class _DummuyResponse(object):
        @staticmethod
        def iter_content():
            """Return dummy data.  """
            return (i.encode('utf-8') for i in dummy_data)
    return_value = _DummuyResponse()
    _add_call(pathname,
              headers={'Range': 'byte={}-'.format(file_size)},
              stream=True, token=token, verify=False)

    server.download(pathname, six.text_type(tmpdir) + '/', token)
