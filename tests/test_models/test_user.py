#!/usr/bin/python3
"""
Unit tests for the User class.
"""

import unittest
import inspect
from datetime import datetime
import pycodestyle
from models import user
from models.base_model import BaseModel
User = user.User


class TestUserDocs(unittest.TestCase):
    """Documentation and PEP8 tests for User."""

    @classmethod
    def setUpClass(cls):
        """Prepare for doc tests."""
        cls.methods = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance(self):
        """Check PEP8 compliance."""
        style_guide = pycodestyle.StyleGuide(quiet=True)
        files = ['models/user.py', 'tests/test_models/test_user.py']
        errors = 0
        for file in files:
            errors += style_guide.check_files([file]).total_errors
        self.assertEqual(errors, 0, "PEP8 issues detected.")

    def test_module_docstring(self):
        """Ensure module docstring presence."""
        self.assertIsNotNone(user.__doc__, "Module docstring is missing.")
        self.assertTrue(len(user.__doc__) > 1)

    def test_class_docstring(self):
        """Check class docstring existence."""
        self.assertIsNotNone(User.__doc__, "Class docstring is missing.")
        self.assertTrue(len(User.__doc__) > 1)

    def test_method_docstrings(self):
        """Validate method docstrings."""
        for name, method in self.methods:
            self.assertIsNotNone(method.__doc__, f"{name} needs a docstring.")
            self.assertTrue(len(method.__doc__) > 1)


class TestUser(unittest.TestCase):
    """Functional tests for User."""

    def test_is_subclass(self):
        """Test subclassing from BaseModel."""
        obj = User()
        self.assertIsInstance(obj, BaseModel)
        self.assertTrue(hasattr(obj, "created_at"))
        self.assertTrue(hasattr(obj, "updated_at"))

    def test_attributes(self):
        """Test attributes and defaults."""
        obj = User()
        attributes = {
            "email": None if models.storage_t == 'db' else "",
            "password": None if models.storage_t == 'db' else "",
            "first_name": None if models.storage_t == 'db' else "",
            "last_name": None if models.storage_t == 'db' else ""
        }
        for attr, expected in attributes.items():
            self.assertTrue(hasattr(obj, attr), f"{attr} is missing.")
            self.assertEqual(getattr(obj, attr), expected)

    def test_to_dict(self):
        """Check dictionary representation."""
        obj = User()
        obj_dict = obj.to_dict()
        expected_keys = ["__class__", "created_at",
                         "updated_at"] + list(obj.__dict__.keys())
        self.assertCountEqual(obj_dict.keys(), expected_keys)
        self.assertEqual(obj_dict['__class__'], 'User')

    def test_dict_values(self):
        """Validate dictionary values format."""
        obj = User()
        obj_dict = obj.to_dict()
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.assertEqual(obj_dict['created_at'],
                         obj.created_at.strftime(time_format))
        self.assertEqual(obj_dict['updated_at'],
                         obj.updated_at.strftime(time_format))

    def test_string_output(self):
        """Test string format of the object representation."""
        obj = User()
        expected_string = f"[User] ({obj.id}) {obj.__dict__}"
        self.assertEqual(str(obj), expected_string)
