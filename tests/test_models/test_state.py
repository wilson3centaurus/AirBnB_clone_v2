#!/usr/bin/python3
"""
Unit tests for the State class.
"""

from datetime import datetime
import inspect
import unittest
import pycodestyle
from models import state
from models.base_model import BaseModel
State = state.State


class TestStateDocs(unittest.TestCase):
    """Documentation and PEP8 compliance tests for State."""

    @classmethod
    def setUpClass(cls):
        """Initialize class for doc tests."""
        cls.methods = inspect.getmembers(State, inspect.isfunction)

    def test_pep8_conformance(self):
        """Verify that code is PEP8 compliant."""
        style_guide = pycodestyle.StyleGuide(quiet=True)
        files = ['models/state.py', 'tests/test_models/test_state.py']
        errors = 0
        for file in files:
            errors += style_guide.check_files([file]).total_errors
        self.assertEqual(errors, 0, "PEP8 issues found.")

    def test_module_docstring(self):
        """Check for the presence of module docstring."""
        self.assertIsNotNone(state.__doc__, "Module docstring is missing.")
        self.assertTrue(len(state.__doc__) > 1)

    def test_class_docstring(self):
        """Check for the presence of class docstring."""
        self.assertIsNotNone(State.__doc__, "Class docstring is missing.")
        self.assertTrue(len(State.__doc__) > 1)

    def test_method_docstrings(self):
        """Ensure all methods have docstrings."""
        for name, method in self.methods:
            self.assertIsNotNone(method.__doc__, f"{
                                 name} method missing docstring.")
            self.assertTrue(len(method.__doc__) > 1)


class TestState(unittest.TestCase):
    """Functional tests for State."""

    def test_subclass_behavior(self):
        """Validate subclassing from BaseModel."""
        obj = State()
        self.assertIsInstance(obj, BaseModel)
        self.assertTrue(hasattr(obj, "created_at"))
        self.assertTrue(hasattr(obj, "updated_at"))

    def test_attributes(self):
        """Test attributes and their defaults."""
        obj = State()
        self.assertTrue(hasattr(obj, "name"))
        expected = None if models.storage_t == 'db' else ""
        self.assertEqual(getattr(obj, "name", type(expected)), expected)

    def test_to_dict(self):
        """Test conversion to dictionary."""
        obj = State()
        obj_dict = obj.to_dict()
        expected_keys = ["__class__", "created_at",
                         "updated_at"] + list(obj.__dict__.keys())
        self.assertCountEqual(obj_dict.keys(), expected_keys)
        self.assertEqual(obj_dict['__class__'], 'State')

    def test_dict_values(self):
        """Validate dictionary values format."""
        obj = State()
        obj_dict = obj.to_dict()
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.assertEqual(obj_dict['created_at'],
                         obj.created_at.strftime(time_format))
        self.assertEqual(obj_dict['updated_at'],
                         obj.updated_at.strftime(time_format))

    def test_string_representation(self):
        """Test string format of object representation."""
        obj = State()
        expected_string = f"[State] ({obj.id}) {obj.__dict__}"
        self.assertEqual(str(obj), expected_string)
