#!/usr/bin/python3
"""Unit tests for states module"""

import inspect
import pep8
import unittest
import os
from api.v1.views import states


class TestStates(unittest.TestCase):
    """Class for testing Hello Route docs"""

    def test_doc(self):
        """Tests module docstring existence"""

        self.assertIsNotNone(states.__doc__)

    def test_function_doc(self):
        """Tests function docstring existence (for all functions)"""

        functions = inspect.getmembers(states, inspect.isfunction)
        for function in functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8(self):
        """Tests if module follows PEP8 style"""

        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['api/v1/views/states.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_executable(self):
        """Tests if the file is executable"""

        file_stat = os.stat('api/v1/views/states.py')
        permissions = str(oct(file_stat[0]))
        expected = int(permissions[5:-2]) >= 5
        self.assertTrue(expected)


if __name__ == "__main__":
    unittest.main()
