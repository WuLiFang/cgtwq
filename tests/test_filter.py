# -*- coding=UTF-8 -*-
"""Test module `cgtwq.filter`.   """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from unittest import TestCase, main

import cgtwq
from cgtwq.filter import Field, Filter, FilterList


class FiltersTestCase(TestCase):
    def test_operations(self):
        result = Filter('title', 'text') | Filter(
            'data', 'test') & Filter('name', 'name')
        self.assertIsInstance(result, FilterList)
        self.assertListEqual(
            result,
            [['title', '=', 'text'],
             'or', ['data', '=', 'test'],
             'and', ['name', '=', 'name']]
        )
        result |= Filter('test2', '233')
        self.assertIsInstance(result, FilterList)
        self.assertListEqual(
            result,
            [['title', '=', 'text'],
             'or', ['data', '=', 'test'],
             'and', ['name', '=', 'name'],
             'or', ['test2', '=', '233']]
        )


class FieldTestCase(TestCase):
    def test_eq(self):
        result = Field('name') == 'john'
        self.assertEqual(result, ['name', '=', 'john'])

    def test_or(self):
        result = Field('name') | 'text1'
        self.assertEqual(result, ['name', 'in', ['text1']])
        result = Field('key') | ('value1', 'value2')
        self.assertEqual(result, ['key', 'in', ('value1', 'value2')])

    def test_and(self):
        result = Field('name') & 'text1'
        self.assertEqual(result, ['name', 'has', 'text1'])

    def test_gt(self):
        result = Field('value') > 3
        self.assertEqual(result, ['value', '>', 3])

    def test_lt(self):
        result = Field('value') < 3
        self.assertEqual(result, ['value', '<', 3])


def test_in_namespace():
    obj1 = cgtwq.Field('key1')
    obj2 = obj1.in_namespace('namespace1')
    assert obj1 == 'key1'
    assert obj2 == 'namespace1.key1'

    obj3 = cgtwq.Filter('key2', 'value2')
    obj4 = obj3.in_namespace('namespace2')
    assert obj3[0] == 'key2'
    assert obj4[0] == 'namespace2.key2'

    obj5 = cgtwq.FilterList(obj3)
    obj6 = obj5.in_namespace('namespace3')
    assert obj5[0][0] == 'key2'
    assert obj6[0][0] == 'namespace3.key2'

    obj7 = cgtwq.FilterList.from_arbitrary_args(obj3, obj4)
    obj8 = obj7.in_namespace('namespace4')
    assert obj7[0][0] == 'key2'
    assert obj8[0][0] == 'namespace4.key2'


def test_from_arbitrary_args():
    result = cgtwq.FilterList.from_arbitrary_args(
        cgtwq.Field('key1') == 'value1')
    assert isinstance(result, FilterList), type(result)
    assert result == [['key1', '=', 'value1']]

    result = cgtwq.FilterList.from_arbitrary_args(
        cgtwq.Field('key1') == 'value1',
        cgtwq.Field('key2') == 'value2')
    assert isinstance(result, FilterList), type(result)
    assert result == [['key1', '=', 'value1'], 'and', ['key2', '=', 'value2']]

    result = cgtwq.FilterList.from_arbitrary_args()
    assert result == []


if __name__ == '__main__':
    main()
