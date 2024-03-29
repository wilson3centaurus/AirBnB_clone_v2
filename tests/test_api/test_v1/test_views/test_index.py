#!/usr/bin/python3
"""Unit tests for v1 app"""

import unittest
import api
import inspect
import pep8
import os


index = api.v1.views.index


class TestIndex(unittest.TestCase):
    """Tests index.py"""

    def test_doc(self):
        """Tests module docstring existence"""

        self.assertIsNotNone(index.__doc__)

    def test_function_doc(self):
        """Tests function docstring existence (for all functions)"""

        functions = inspect.getmembers(index, inspect.isfunction)
        for function in functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8(self):
        """Tests if module follows PEP8 style"""

        style = pep8.StyleGuide(quiet=True)
        errors = style.check_files(['api/v1/views/index.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_executable(self):
        """Tests if the file is executable"""

        stat = os.stat('api/v1/views/index.py')
        permissions = str(oct(stat[0]))
        expected = int(permissions[5:-2]) >= 5
        self.assertTrue(expected)
