# -*- coding=UTF-8 -*-
"""Exceptions for cgtwq.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

if six.PY2:
    _BYTES_KEY = b'__str__'
    _STR_KEY = b'__unicode__'
else:
    _BYTES_KEY = '__bytes__'
    _STR_KEY = '__str__'


def _as_suffix(list_):
    if not list_:
        return '.'
    msg = list_[0] if len(list_) == 1 else list_
    return ': {}'.format(msg)


def _template_meta(__bytes__, __str__):

    class _TemplateMetaClass(type):
        def __new__(mcs, name, bases, dict_):
            dict_[_BYTES_KEY] = lambda self: (
                __bytes__ + _as_suffix(self.args)).encode('utf-8')
            dict_[_STR_KEY] = lambda self: __str__ + _as_suffix(self.args)
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


@six.add_metaclass(
    _template_meta(
        'Empty selection',
        '空条目选择'))
class EmptySelection(CGTeamWorkException, ValueError):
    """Indicate no entry match the criteria."""

    def __init__(self):
        super(EmptySelection, self).__init__('Empty selection.')


@six.add_metaclass(_template_meta('Wrong password', '密码错误'))
class PasswordError(CGTeamWorkException):
    """Indicate password not correct.  """


@six.add_metaclass(_template_meta('Account not found', '无此帐号'))
class AccountNotFoundError(CGTeamWorkException):
    """Indicate account not found.  """


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


@six.add_metaclass(  # pylint: disable=redefined-builtin
    _template_meta(
        'Sufficient permission',
        '权限不足'))
class PermissionError(CGTeamWorkException):
    """Indicate sufficient permission.  """
