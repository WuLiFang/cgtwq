# -*- coding=UTF-8 -*-
"""Test module `cgtwq.database`."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import io
import os
import uuid
from tempfile import mkdtemp, mkstemp
from unittest import TestCase, main

from util import skip_if_not_logged_in
from cgtwq import server, DesktopClient
import cgtwq


@skip_if_not_logged_in
class ServerTestCase(TestCase):
    def test_account(self):
        token = cgtwq.DesktopClient.token()
        account = cgtwq.get_account(token)
        account_id = cgtwq.get_account_id(token)
        print('# account: <id: {}: {}>'.format(account_id, account))

    def test_file_operation(self):
        # Prepare
        tempdir = mkdtemp()
        self.addCleanup(os.rmdir, tempdir)
        fd, tempfile = mkstemp(dir=tempdir)
        self.addCleanup(os.remove, tempfile)
        dummy_data = unicode(uuid.uuid4())
        with io.open(fd, 'w') as f:
            f.write(dummy_data)
        dir_pathname = '/_pytest_{}'.format(dummy_data)
        filename = '{}.pytemp'.format(dummy_data)
        token = DesktopClient.token()

        # Do test.

        # `mkdir`, `exists`, 'isdir'.
        self.assertIs(server.exists(dir_pathname, token), False)
        server.mkdir(dir_pathname, token)
        self.assertIs(server.exists(dir_pathname, token), True)
        self.assertIs(server.isdir(dir_pathname, token), True)

        # `upload`, `exists`, 'isdir'.
        pathname = '{}/{}'.format(dir_pathname, filename)
        self.assertIs(server.exists(pathname, token), False)
        server.upload(tempfile, pathname, token)
        self.assertIs(server.exists(pathname, token), True)
        self.assertIs(server.isdir(pathname, token), False)

        # `rename`.
        temppathname = '{}.rename'.format(pathname)
        server.rename(pathname, temppathname, token)
        self.assertIs(server.exists(temppathname, token), True)
        self.assertIs(server.exists(filename, token), False)
        server.rename(temppathname, pathname, token)
        self.assertIs(server.exists(pathname, token), True)
        self.assertIs(server.exists(temppathname, token), False)

        # `download`.
        downloaded = server.download(pathname, tempdir + '/', token)
        self.assertIn(filename, server.listdir(dir_pathname, token).file)
        with open(downloaded) as f:
            self.assertEqual(f.read(), dummy_data)
        self.addCleanup(os.remove, downloaded)

        # `delete`, `exists`, 'isdir'.
        server.delete(pathname, token)
        self.assertNotIn(filename, server.listdir(dir_pathname, token).file)
        server.delete(dir_pathname, token)
        self.assertIs(server.exists(dir_pathname, token), False)

    def test_login(self):
        self.assertRaises(ValueError, cgtwq.login, 'admin', 'default')


if __name__ == '__main__':
    main()
