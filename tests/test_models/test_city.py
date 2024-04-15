#!/usr/bin/python3
"""Tests for the City class."""

import unittest
import inspect
from models import city
from models.base_model import BaseModel
import pycodestyle

City = city.City


class TestCityDocs(unittest.TestCase):
    """Documentation and PEP8 compliance tests for City."""

    @classmethod
    def setUpClass(cls):
        """Prepare for testing documentation."""
        cls.funcs = inspect.getmembers(City, inspect.isfunction)

    def test_pep8_conformance(self):
        """Verify that code conforms to PEP8."""
        files = ['models/city.py', 'tests/test_models/test_city.py']
        pep8_style = pycodestyle.StyleGuide(quiet=True)
        errors = sum(pep8_style.check_files(files).total_errors)
        self.assertEqual(errors, 0, "PEP8 style errors detected.")

    def test_docs(self):
        """Check for module and class documentation."""
        self.assertTrue(len(city.__doc__) >= 1, "Module docstring required.")
        self.assertTrue(len(City.__doc__) >= 1, "Class docstring required.")

    def test_method_docs(self):
        """Ensure all public methods have docstrings."""
        for func_name, func in self.funcs:
            self.assertTrue(len(func.__doc__) >= 1, f"{
                            func_name} missing docstring.")


class TestCity(unittest.TestCase):
    """Unit tests for the City class."""

    def test_subclass(self):
        """Validate that City is a BaseModel subclass."""
        obj = City()
        self.assertIsInstance(obj, BaseModel)
        self.assertTrue(hasattr(obj, "id"))

    def test_attributes(self):
        """Test attributes exist and have correct default values."""
        obj = City()
        self.assertTrue(hasattr(obj, "name"))
        self.assertEqual(obj.name, None if models.storage_t == 'db' else "")

        self.assertTrue(hasattr(obj, "state_id"))
        self.assertEqual(
            obj.state_id, None if models.storage_t == 'db' else "")

    def test_to_dict(self):
        """Test conversion to dictionary."""
        obj = City()
        dict_repr = obj.to_dict()
        expected_keys = ["__class__", "created_at",
                         "updated_at"] + list(obj.__dict__.keys())
        self.assertCountEqual(dict_repr.keys(), expected_keys)
        self.assertEqual(dict_repr["__class__"], "City")

    def test_to_dict_values(self):
        """Validate dictionary values."""
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        obj = City()
        dict_repr = obj.to_dict()
        self.assertEqual(dict_repr["created_at"],
                         obj.created_at.strftime(time_format))
        self.assertEqual(dict_repr["updated_at"],
                         obj.updated_at.strftime(time_format))

    def test_string_representation(self):
        """Test the string representation of City."""
        obj = City()
        expected_str = f"[City] ({obj.id}) {obj.__dict__}"
        self.assertEqual(str(obj), expected_str)
