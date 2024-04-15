#!/usr/bin/python3
"""Test cases for the Amenity class."""

import unittest
import inspect
import pycodestyle
from models import amenity
from models.base_model import BaseModel

Amenity = amenity.Amenity


class TestAmenityDocs(unittest.TestCase):
    """Documentation and PEP8 tests for Amenity."""

    @classmethod
    def setUpClass(cls):
        """Setup for doc tests."""
        cls.funcs = inspect.getmembers(Amenity, inspect.isfunction)

    def test_pep8_conformance(self):
        """PEP8 style checks."""
        style = pycodestyle.StyleGuide(quiet=True)
        model_result = style.check_files(['models/amenity.py'])
        test_result = style.check_files(['tests/test_models/test_amenity.py'])
        self.assertEqual(model_result.total_errors, 0, "PEP8 issues in model.")
        self.assertEqual(test_result.total_errors, 0, "PEP8 issues in tests.")

    def test_docs(self):
        """Documentation existence tests."""
        self.assertIsNotNone(amenity.__doc__, "Missing module docstring.")
        self.assertTrue(len(amenity.__doc__) >= 1)
        self.assertIsNotNone(Amenity.__doc__, "Missing class docstring.")
        self.assertTrue(len(Amenity.__doc__) >= 1)

    def test_method_docs(self):
        """Method documentation tests."""
        for name, func in self.funcs:
            self.assertIsNotNone(func.__doc__, f"{name} missing docstring.")


class TestAmenity(unittest.TestCase):
    """Functional tests for Amenity."""

    def test_subclass(self):
        """Test Amenity subclass type."""
        obj = Amenity()
        self.assertIsInstance(obj, BaseModel)
        self.assertTrue(hasattr(obj, "id"))
        self.assertTrue(hasattr(obj, "created_at"))
        self.assertTrue(hasattr(obj, "updated_at"))

    def test_name_attr(self):
        """Amenity name attribute test."""
        obj = Amenity()
        expected = None if models.storage_t == 'db' else ""
        self.assertEqual(getattr(obj, 'name', type(expected)), expected)

    def test_to_dict(self):
        """Test dictionary representation."""
        obj = Amenity()
        dict_rep = obj.to_dict()
        self.assertIsInstance(dict_rep, dict)
        self.assertNotIn("_sa_instance_state", dict_rep)
        self.assertIn("__class__", dict_rep)
        self.check_dict_contains(dict_rep, obj)

    def check_dict_contains(self, dict_rep, obj):
        """Check dictionary attributes."""
        for key in obj.__dict__:
            if key != "_sa_instance_state":
                self.assertIn(key, dict_rep)
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.assertEqual(dict_rep["created_at"],
                         obj.created_at.strftime(t_format))
        self.assertEqual(dict_rep["updated_at"],
                         obj.updated_at.strftime(t_format))

    def test_str_method(self):
        """String method test."""
        obj = Amenity()
        expected_str = f"[Amenity] ({obj.id}) {obj.__dict__}"
        self.assertEqual(expected_str, str(obj))
