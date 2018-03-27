# -*- coding=UTF-8 -*-
"""Exceptions for cgtwq.  """

from __future__ import absolute_import, unicode_literals, print_function


class CGTeamWorkException(Exception):
    """Base exception class for CGTeamWork.  """

    def __init__(self, *args):
        super(CGTeamWorkException, self).__init__()
        self.message = args


class IDError(CGTeamWorkException):
    """Indicate can't specify shot id on cgtw."""

    def __str__(self):
        return 'Can not found item with matched id:{}'.format(self.message)

    def __unicode__(self):
        return '找不到数据库对象: {}'.format(self.message)


class SignError(CGTeamWorkException):
    """Indicate can't found matched sign."""

    def __str__(self):
        return 'Can not found matched sign: {}'.format(self.message)

    def __unicode__(self):
        return '缺少数据库标志: {}'.format(self.message)


class FolderError(CGTeamWorkException):
    """Indicate can't found destination folder."""

    def __str__(self):
        return 'No such folder on server: {}'.format(self.message)

    def __unicode__(self):
        return '不存在服务器文件夹: {}'.format(self.message)


class LoginError(CGTeamWorkException):
    """Indicate can't found destination folder."""

    def __str__(self):
        return 'Not loged in.  \n{}'.format(self.message)

    def __unicode__(self):
        return '未登录或登录失效: {}'.format(self.message)


class PrefixError(CGTeamWorkException):
    """Indicate ."""

    def __init__(self, prefix):
        super(PrefixError, self).__init__(prefix)
        self.prefix = prefix

    def __str__(self):
        return 'Can not found any prefix matched shots: {}'.format(self.prefix)

    def __unicode__(self):
        return '无镜头匹配此前缀: {}'.format(self.message)


class AccountError(CGTeamWorkException):
    """Indicate can't found destination folder."""

    def __init__(self, owner='', current=''):
        CGTeamWorkException.__init__(self)
        self.owner = owner
        self.current = current

    def __str__(self):
        return 'Account not match.  \n{} ==> {}'.format(self.current, self.owner)

    def __unicode__(self):
        return '用户不匹配\n\t已分配给:\t{}\n\t当前用户:\t{}'.format(self.owner or '<未分配>', self.current)
