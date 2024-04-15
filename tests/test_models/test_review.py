#!/usr/bin/python3
"""
Unit tests for the Review class.
"""

from datetime import datetime
import inspect
import unittest
import pycodestyle
from models import review
from models.base_model import BaseModel
Review = review.Review


class TestReviewDocs(unittest.TestCase):
    """Documentation and PEP8 tests for Review class."""

    @classmethod
    def setUpClass(cls):
        """Initialize class for doc tests."""
        cls.funcs = inspect.getmembers(Review, inspect.isfunction)

    def test_pep8_conformance(self):
        """Check PEP8 compliance for review files."""
        files = ['models/review.py', 'tests/test_models/test_review.py']
        pep8_style = pycodestyle.StyleGuide(quiet=True)
        result = sum(file.check_files([f]).total_errors for f in files)
        self.assertEqual(result, 0, "PEP8 errors found.")

    def test_module_docstring(self):
        """Ensure module docstring exists."""
        self.assertIsNotNone(review.__doc__, "Module docstring is missing.")
        self.assertTrue(len(review.__doc__) >= 1)

    def test_class_docstring(self):
        """Ensure class docstring exists."""
        self.assertIsNotNone(Review.__doc__, "Class docstring is missing.")
        self.assertTrue(len(Review.__doc__) >= 1)

    def test_method_docstrings(self):
        """Check for method docstrings."""
        for name, func in self.funcs:
            self.assertIsNotNone(func.__doc__, f"{name} needs a docstring.")
            self.assertTrue(len(func.__doc__) >= 1)


class TestReview(unittest.TestCase):
    """Functional tests for the Review class."""

    def test_subclass(self):
        """Verify that Review is a subclass of BaseModel."""
        obj = Review()
        self.assertIsInstance(obj, BaseModel)
        self.assertTrue(hasattr(obj, "created_at"))
        self.assertTrue(hasattr(obj, "updated_at"))

    def test_attributes(self):
        """Test attribute existence and default values."""
        obj = Review()
        attributes = {
            "place_id": "" if models.storage_t != 'db' else None,
            "user_id": "" if models.storage_t != 'db' else None,
            "text": "" if models.storage_t != 'db' else None
        }
        for attr, expected in attributes.items():
            self.assertTrue(hasattr(obj, attr), f"{attr} is missing.")
            self.assertEqual(getattr(obj, attr), expected)

    def test_to_dict(self):
        """Check dictionary conversion."""
        obj = Review()
        obj_dict = obj.to_dict()
        expected_keys = ["__class__", "created_at",
                         "updated_at"] + list(obj.__dict__.keys())
        self.assertCountEqual(obj_dict.keys(), expected_keys)
        self.assertEqual(obj_dict['__class__'], 'Review')

    def test_dict_values(self):
        """Validate to_dict values format."""
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        obj = Review()
        obj_dict = obj.to_dict()
        self.assertEqual(obj_dict['created_at'],
                         obj.created_at.strftime(time_format))
        self.assertEqual(obj_dict['updated_at'],
                         obj.updated_at.strftime(time_format))

    def test_string_output(self):
        """Test the string representation of the object."""
        obj = Review()
        expected_string = f"[Review] ({obj.id}) {obj.__dict__}"
        self.assertEqual(str(obj), expected_string)
