#!/usr/bin/python3
"""
Unit tests for the console module.
"""

import unittest
import pycodestyle
import console
from console import HBNBCommand


class TestConsoleDocs(unittest.TestCase):
    """Tests for ensuring documentation and coding style for the console."""

    def test_pep8_conformance(self):
        """Verify that the console files conform to PEP8."""
        pep8_style = pycodestyle.StyleGuide(quiet=True)
        files_to_check = ['console.py', 'tests/test_console.py']
        errors = sum(pep8_style.check_files(
            files_to_check).total_errors for file in files_to_check)
        self.assertEqual(errors, 0, "PEP8 style errors or warnings exist.")

    def test_module_docstring(self):
        """Check for the presence of a module docstring."""
        self.assertIsNotNone(
            console.__doc__, "Missing docstring in the console module.")
        self.assertTrue(len(console.__doc__) > 1,
                        "Console module docstring is too short.")

    def test_class_docstring(self):
        """Ensure the HBNBCommand class has a proper docstring."""
        self.assertIsNotNone(HBNBCommand.__doc__,
                             "Missing docstring in the HBNBCommand class.")
        self.assertTrue(len(HBNBCommand.__doc__) > 1,
                        "HBNBCommand class docstring is too short.")
