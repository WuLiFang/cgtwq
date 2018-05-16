# -*- coding=UTF-8 -*-
"""Exceptions for cgtwq.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six


def _as_suffix(list_):
    if not list_:
        return '.'
    msg = list_[0] if len(list_) == 1 else list_
    return ': {}'.format(msg)


def _template_meta(__bytes__, __str__):

    class _TemplateMetaClass(type):
        def __new__(mcs, name, bases, dict_):
            dict_[b'__str__' if six.PY2 else '__bytes__'] = lambda self: (
                __bytes__ + _as_suffix(self.args)).encode('utf-8')
            dict_[b'__unicode__'if six.PY2 else '__str__'] = lambda self: (
                __str__ + _as_suffix(self.args))
            return type.__new__(mcs, name, bases, dict_)

    return _TemplateMetaClass


class CGTeamWorkException(Exception):
    """Base exception class for CGTeamWork.  """


@six.add_metaclass(
    _template_meta(
        'Can not found item with matched id',
        '找不到数据库对象'))
class IDError(CGTeamWorkException):
    """Indicate can't specify shot id on cgtw."""


@six.add_metaclass(
    _template_meta(
        'Can not found matched sign',
        '缺少数据库标志'))
class SignError(CGTeamWorkException):
    """Indicate can't found matched sign."""


@six.add_metaclass(
    _template_meta(
        'No such folder on server',
        '不存在服务器文件夹'))
class FolderError(CGTeamWorkException):
    """Indicate can't found destination folder.  """


@six.add_metaclass(
    _template_meta(
        'Not loged in',
        '未登录或登录失效'))
class LoginError(CGTeamWorkException):
    """Indicate not logged in.  """


@six.add_metaclass(
    _template_meta(
        'Can not found any prefix matched shots',
        '无镜头匹配此前缀'))
class PrefixError(CGTeamWorkException):
    """Indicate no shot match the prefix."""


@six.add_metaclass(_template_meta('Wrong password', '密码错误'))
class PasswordError(CGTeamWorkException):
    """Inicate password not correct.  """


@six.add_metaclass(_template_meta('Account not found', '无此帐号'))
class AccountNotFoundError(CGTeamWorkException):
    """Inicate account not found.  """


class AccountError(CGTeamWorkException):
    """Indicate account not match."""

    def __init__(self, owner='', current=''):
        CGTeamWorkException.__init__(self)
        self.owner = owner
        self.current = current

    def __str__(self):
        return 'Account not match.  \n{} ==> {}'.format(self.current, self.owner)

    def __unicode__(self):
        return '用户不匹配\n\t已分配给:\t{}\n\t当前用户:\t{}'.format(self.owner or '<未分配>', self.current)
