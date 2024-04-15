#!/usr/bin/python3
"""
Tests for Place class.
"""

from datetime import datetime
import unittest
import inspect
import models
from models import place
from models.base_model import BaseModel
import pycodestyle
Place = place.Place


class TestPlaceDocs(unittest.TestCase):
    """Documentation and style tests for the Place class."""

    @classmethod
    def setUpClass(cls):
        """Setup for documentation tests."""
        cls.funcs = inspect.getmembers(Place, inspect.isfunction)

    def test_pep8_conformance(self):
        """Check that code is PEP8 compliant."""
        style_guide = pycodestyle.StyleGuide(quiet=True)
        files = ['models/place.py', 'tests/test_models/test_place.py']
        errors = 0
        for file in files:
            errors += style_guide.check_files([file]).total_errors
        self.assertEqual(errors, 0, "PEP8 issues found.")

    def test_module_docstring(self):
        """Check for the existence of module docstring."""
        self.assertIsNotNone(place.__doc__, "Missing module docstring.")
        self.assertTrue(len(place.__doc__) >= 1)

    def test_class_docstring(self):
        """Check for the existence of Place class docstring."""
        self.assertIsNotNone(Place.__doc__, "Missing class docstring.")
        self.assertTrue(len(Place.__doc__) >= 1)

    def test_function_docstrings(self):
        """Check for the existence of docstrings in all functions."""
        for func_name, func in self.funcs:
            self.assertIsNotNone(func.__doc__, f"{func_name} needs docstring.")
            self.assertTrue(len(func.__doc__) >= 1)


class TestPlace(unittest.TestCase):
    """Test suite for Place class."""

    def test_is_subclass(self):
        """Test that Place is a subclass of BaseModel."""
        obj = Place()
        self.assertIsInstance(obj, BaseModel)
        self.assertTrue(hasattr(obj, "created_at"))
        self.assertTrue(hasattr(obj, "updated_at"))

    def test_attributes(self):
        """Test attributes with expected types and default values."""
        obj = Place()
        attributes = {
            "city_id": None if models.storage_t == 'db' else "",
            "user_id": None if models.storage_t == 'db' else "",
            "name": None if models.storage_t == 'db' else "",
            "description": None if models.storage_t == 'db' else "",
            "number_rooms": int,
            "number_bathrooms": int,
            "max_guest": int,
            "price_by_night": int,
            "latitude": float,
            "longitude": float,
            "amenity_ids": list
        }
        for attr, typ in attributes.items():
            self.assertTrue(hasattr(obj, attr), f"Missing {attr} attribute.")
            value = getattr(obj, attr)
            if typ in (int, float) and models.storage_t != 'db':
                self.assertIsInstance(value, typ)
                self.assertEqual(value, 0 if typ is int else 0.0)
            elif typ is list:
                self.assertIsInstance(value, list)
                self.assertEqual(len(value), 0)
            else:
                self.assertEqual(value, typ)

    def test_to_dict(self):
        """Test that to_dict method converts to dictionary properly."""
        obj = Place()
        obj_dict = obj.to_dict()
        expected_attrs = ["id", "created_at", "updated_at",
                          "__class__"] + list(obj.__dict__.keys())
        self.assertCountEqual(obj_dict.keys(), expected_attrs)
        self.assertEqual(obj_dict['__class__'], 'Place')

    def test_to_dict_values(self):
        """Ensure dictionary values match object attributes."""
        obj = Place()
        obj_dict = obj.to_dict()
        fmt = "%Y-%m-%dT%H:%M:%S.%f"
        self.assertEqual(obj_dict['created_at'], obj.created_at.strftime(fmt))
        self.assertEqual(obj_dict['updated_at'], obj.updated_at.strftime(fmt))

    def test_string_representation(self):
        """Test the string representation of the object."""
        obj = Place()
        expected_str = f"[Place] ({obj.id}) {obj.__dict__}"
        self.assertEqual(str(obj), expected_str)
