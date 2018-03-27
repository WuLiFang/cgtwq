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

from .http import post, get
from ..client import CGTeamWorkClient
from ..util import file_md5

LOGGER = logging.getLogger(__name__)

BACKUP = 1 << 0
COUNTINUE = 1 << 1
REPLACE = 1 << 2


def upload(path, pathname, ip=None, flags=BACKUP | COUNTINUE):
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

    chunk_size = 2*2**20  # 2MB
    hash_ = file_md5(path)
    pathname = '/{}'.format(unicode(pathname).lstrip('\\/'))
    ip = ip or CGTeamWorkClient.server_ip()
    ret = 'http://{}{}'.format(ip, pathname)

    LOGGER.debug('upload: %s -> %s', path, pathname)
    result = post('/file.php', {'file_md5': hash_,
                                'upload_des_path': pathname,
                                'action': 'pre_upload'},
                  ip=ip)
    LOGGER.debug('POST: result: %s', result)

    assert isinstance(result, dict)
    if result.get('upload'):
        # Same file alreay uploaded.
        return ret
    if result['is_exist'] and not flags & REPLACE:
        raise ValueError('File already exists.')

    file_size = os.path.getsize(path)
    if not file_size:
        raise ValueError('File is empty.')

    file_pos = result['file_pos']
    with open(path, 'rb') as f:
        if file_pos:
            f.seek(file_pos)
        data = {'file_md5': hash_,
                'file_size': file_size,
                'upload_des_path': pathname,
                'is_backup_to_history': 'Y' if flags & BACKUP else 'N',
                'no_continue_upload': 'N' if flags & COUNTINUE else 'Y'}
        for chunk in iter(lambda: f.read(chunk_size), b''):
            data['read_pos'] = file_pos
            post('/upload_file', data, files={'files': chunk})
            file_pos += chunk_size

    return ret


def download(pathname, dest):
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

    info = stat(pathname)
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
    resp = get(info.server_path, stream=True, verify=False, headers=headers)
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


def file_operation(action, **kwargs):
    """Do file operation on server.

    Args:
        action (unicode): Server defined action name.

    Returns:
        Server execution result.
    """

    LOGGER.debug('%s: %s', action, kwargs)
    kwargs['action'] = action
    result = post('/file.php', kwargs)
    LOGGER.debug('%s: result: %s', action, result)
    return result


def delete(pathname):
    """Delete file on server.

    Args:
        pathname (unicode): Server pathname.

    Returns:
        bool: Is deletion successed.
    """

    return file_operation('delete', server_path=pathname)


def rename(src, dst):
    """Rename(move) file on server.

    Args:
        src (unicode): Source server pathname.
        dst (unicode): Destnation server pathname.

    Returns:
        bool: Is deletion successed.
    """

    return file_operation('rename', old_path=src, new_path=dst)


def mkdir(pathname):
    """Make directory on server.

    Args:
        pathname (unicode): Server pathname.

    Returns:
        bool: Is directory created.
    """

    return file_operation('create_dir', server_path=pathname)


DirInfo = namedtuple('DirInfo', ('dir', 'file'))


def listdir(pathname):
    """List directory contents on server.

    Args:
        pathname (unicode): Server pathname

    Returns:
        DirInfo: namedtuple of directory info.
    """

    result = file_operation('list_dir', server_path=pathname)
    return DirInfo(**result)


def isdir(pathname):
    """Check if pathname is directory.

    Args:
        pathname (unicode): Server pathname.

    Returns:
        bool: True if `pathname` is directory.
    """

    return file_operation('is_dir', server_path=pathname)


def exists(pathname):
    """Check if pathname exists on server.

    Args:
        pathname (unicode): Server pathname.

    Returns:
        bool: True if `pathname` exists on server.
    """

    return file_operation('file_exists', server_path=pathname)


FileInfo = namedtuple('FileInfo', ('file_md5', 'file_size', 'server_path'))


def stat(pathname):
    """Get server file status.

    Args:
        pathname (unicode): Server pathname.

    Returns:
        FileInfo: Server file information.
    """

    result = file_operation('file_info', server_path=pathname)
    assert isinstance(result, dict), type(result)
    return FileInfo(**result)
