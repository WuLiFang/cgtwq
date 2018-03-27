# -*- coding=UTF-8 -*-
"""Test module `cgtwq.filter`.   """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from unittest import TestCase, main

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


if __name__ == '__main__':
    main()
