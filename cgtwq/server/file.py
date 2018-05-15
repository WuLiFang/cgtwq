# -*- coding=UTF-8 -*-
"""Manipulate files on server.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import errno
import io
import logging
import os
import tempfile
from collections import namedtuple

from six import text_type

from .filetools import file_md5
from .http import get, post

LOGGER = logging.getLogger(__name__)

BACKUP = 1 << 0
COUNTINUE = 1 << 1
REPLACE = 1 << 2

UPLOAD_CHUNK_SIZE = 2*2**20  # 2MB


def upload(path, pathname, token, ip=None, flags=BACKUP | COUNTINUE):
    """Upload file to server.

    Args:
        path (unicode): Local file path.
        pathname (unicode): Server pathname.
        flags(BACKUP, COUNTINUE, REPLACE):
            Defaults to `BACKUP | COUNTINUE`.
            `BACKUP`: Tell server backup to history or not.
            `COUNTINUE`: If set, will continue previous upload(if exists).
            `REPLACE`: If set, will replace exsited server file.

    Raises:
        ValueError: When server file exists and `REPLACE` flag is not set.
        ValueError: When local file is empty.

    Returns:
        str: Upload path.
    """
    # pylint: disable=invalid-name

    pathname = '/{}'.format(unicode(pathname).lstrip('\\/'))
    _post_file(path, pathname, token, ip, flags)
    return 'http://{}{}'.format(ip, pathname)


def _prepare_upload(path, pathname, token, ip):
    """Prepare upload. """

    file_size = os.path.getsize(path)
    if not file_size:
        raise ValueError('File is empty.')
    hash_ = file_md5(path)
    result = post('/file.php',
                  {'file_md5': hash_,
                   'upload_des_path': pathname,
                   'action': 'pre_upload'},
                  token=token,
                  ip=ip)
    LOGGER.debug('POST: result: %s', text_type(result))
    assert isinstance(result, dict)
    data_class = namedtuple(
        'PostPrepareData', ('md5', 'size', 'pos', 'is_exists', 'is_uploaded'))
    return data_class(md5=hash_,
                      size=file_size,
                      pos=result.get('file_pos'),
                      is_exists=result.get('is_exist'),
                      is_uploaded=result.get('upload'))


def _post_file(path, pathname, token, ip, flags):
    """Prepare and upload file to server.  """

    prepare_data = _prepare_upload(path, pathname, token, ip)
    if prepare_data.is_exists and not flags & REPLACE:
        raise ValueError('File already exists.')
    if prepare_data.is_uploaded:
        return
    data = {'file_md5': prepare_data.md5,
            'file_size': prepare_data.size,
            'upload_des_path': pathname,
            'is_backup_to_history': 'Y' if flags & BACKUP else 'N',
            'no_continue_upload': 'N' if flags & COUNTINUE else 'Y'}
    with open(path, 'rb') as f:
        pos = prepare_data.pos
        f.seek(pos)
        for chunk in iter(lambda: f.read(UPLOAD_CHUNK_SIZE), b''):
            data['read_pos'] = pos
            post('/upload_file', data, token=token,
                 files={'files': chunk})
            pos += UPLOAD_CHUNK_SIZE


def download(pathname, dest, token):
    """Download file from server.

    Args:
        pathname (unicode): Server host pathname. (e.g. `/upload/somefile.txt`)
        dest (unicode): Local destination path.
            if `dest` ends with `\\` or `/`, will treat dest as directory.

    Raises:
        ValueError: When server file not exists.
        ValueError: Local file already exists.
        RuntimeError: Dowanload fail.

    Returns:
        unicode: Path of downloaded file.
    """

    info = stat(pathname, token)
    if not info.file_md5:
        raise ValueError('Server file not exists.', pathname)

    # Convert diraname as dest.
    if unicode(dest).endswith(('\\', '/')):
        dest = os.path.abspath(
            os.path.join(
                dest, os.path.basename(info.server_path)
            )
        )

    # Skip if already downloaded.
    if os.path.exists(dest):
        if os.path.isfile(dest) and file_md5(dest) == info.file_md5:
            return dest
        else:
            raise ValueError('Local file already exists.', dest)

    # Create dest_dir.
    dest_dir = os.path.dirname(dest)
    try:
        os.makedirs(dest_dir)
    except OSError as ex:
        if ex.errno not in (errno.EEXIST, errno.EACCES):
            raise

    # Download to tempfile.
    headers = {'Range': 'byte={}-'.format(info.file_size)}
    resp = get(info.server_path, token=token,
               stream=True, verify=False, headers=headers)
    fd, filename = tempfile.mkstemp('.cgtwqdownload', dir=dest_dir)
    with io.open(fd, 'wb') as f:
        for chunk in resp.iter_content():
            f.write(chunk)

    # Check hash of downloaded file.
    if file_md5(filename) != info.file_md5:
        os.remove(filename)
        raise RuntimeError('Downloaded content not match server md5.')

    os.rename(filename, dest)
    return dest


def file_operation(action, token, **kwargs):
    """Do file operation on server.

    Args:
        action (str): Server defined action name.
        token (str): User token.

    Returns:
        Server execution result.
    """

    LOGGER.debug('%s: %s', action, kwargs)
    kwargs['action'] = action
    result = post('/file.php', data=kwargs, token=token)
    LOGGER.debug('%s: result: %s', action, result)
    return result


def delete(pathname, token):
    """Delete file on server.

    Args:
        pathname (unicode): Server pathname.

    Returns:
        bool: Is deletion successed.
    """

    return file_operation('delete', token=token, server_path=pathname)


def rename(src, dst, token):
    """Rename(move) file on server.

    Args:
        src (unicode): Source server pathname.
        dst (unicode): Destnation server pathname.

    Returns:
        bool: Is deletion successed.
    """

    return file_operation('rename', token=token, old_path=src, new_path=dst)


def mkdir(pathname, token):
    """Make directory on server.

    Args:
        pathname (unicode): Server pathname.

    Returns:
        bool: Is directory created.
    """

    return file_operation('create_dir', token=token, server_path=pathname)


DirInfo = namedtuple('DirInfo', ('dir', 'file'))


def listdir(pathname, token):
    """List directory contents on server.

    Args:
        pathname (unicode): Server pathname

    Returns:
        DirInfo: namedtuple of directory info.
    """

    result = file_operation('list_dir', token=token, server_path=pathname)
    return DirInfo(**result)


def isdir(pathname, token):
    """Check if pathname is directory.

    Args:
        pathname (unicode): Server pathname.

    Returns:
        bool: True if `pathname` is directory.
    """

    return file_operation('is_dir', token=token, server_path=pathname)


def exists(pathname, token):
    """Check if pathname exists on server.

    Args:
        pathname (unicode): Server pathname.

    Returns:
        bool: True if `pathname` exists on server.
    """

    return file_operation('file_exists', token=token, server_path=pathname)


FileInfo = namedtuple('FileInfo', ('file_md5', 'file_size', 'server_path'))


def stat(pathname, token):
    """Get server file status.

    Args:
        pathname (unicode): Server pathname.

    Returns:
        FileInfo: Server file information.
    """

    result = file_operation('file_info', token=token, server_path=pathname)
    assert isinstance(result, dict), type(result)
    return FileInfo(**result)
