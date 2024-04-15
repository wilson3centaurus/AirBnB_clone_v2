#!/usr/bin/python3
"""Tests for the BaseModel class."""

import unittest
from datetime import datetime
import time
import inspect
import models
from unittest import mock
import pycodestyle
from models.base_model import BaseModel


class TestBaseModelDocs(unittest.TestCase):
    """Documentation and PEP8 tests for BaseModel."""

    @classmethod
    def setUpClass(cls):
        """Setup for doc tests."""
        cls.base_methods = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Check PEP8 style."""
        paths = ['models/base_model.py',
                 'tests/test_models/test_base_model.py']
        for path in paths:
            with self.subTest(path=path):
                checker = pycodestyle.Checker(path)
                errors = checker.check_all()
                self.assertEqual(errors, 0)

    def test_docs(self):
        """Module and class docstrings tests."""
        self.assertIsNotNone(models.base_model.__doc__)
        self.assertTrue(len(models.base_model.__doc__) > 1)
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertTrue(len(BaseModel.__doc__) > 1)

    def test_method_docs(self):
        """Method docstring tests."""
        for method_name, method in self.base_methods:
            with self.subTest(method=method_name):
                self.assertIsNotNone(method.__doc__)
                self.assertTrue(len(method.__doc__) > 1)


class TestBaseModel(unittest.TestCase):
    """Functional tests for BaseModel."""

    def test_instantiation(self):
        """Object creation test."""
        instance = BaseModel()
        self.assertIsInstance(instance, BaseModel)
        instance.name = "Holberton"
        instance.number = 89
        attributes = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        for attribute, attr_type in attributes.items():
            with self.subTest(attribute=attribute):
                self.assertIn(attribute, instance.__dict__)
                self.assertIs(type(instance.__dict__[attribute]), attr_type)
        self.assertEqual(instance.name, "Holberton")
        self.assertEqual(instance.number, 89)

    def test_datetime_attributes(self):
        """Datetime attributes test."""
        instance1 = BaseModel()
        instance2 = BaseModel()
        time.sleep(0.1)
        self.assertNotEqual(instance1.created_at, instance2.created_at)
        self.assertEqual(instance1.created_at, instance1.updated_at)
        self.assertNotEqual(instance1.updated_at, instance2.updated_at)

    def test_uuid(self):
        """UUID format validation."""
        instance1 = BaseModel()
        instance2 = BaseModel()
        uuid_regex = '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        for instance in [instance1, instance2]:
            with self.subTest(uuid=instance.id):
                self.assertRegex(instance.id, uuid_regex)
        self.assertNotEqual(instance1.id, instance2.id)

    def test_to_dict(self):
        """Dictionary representation test."""
        model = BaseModel()
        model.name = "Holberton"
        model.my_number = 89
        model_dict = model.to_dict()
        expected_keys = ["id", "created_at", "updated_at",
                         "name", "my_number", "__class__"]
        self.assertCountEqual(model_dict.keys(), expected_keys)
        self.assertEqual(model_dict['__class__'], 'BaseModel')

    def test_to_dict_values(self):
        """Validate dictionary values."""
        format = "%Y-%m-%dT%H:%M:%S.%f"
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertEqual(model_dict["created_at"],
                         model.created_at.strftime(format))
        self.assertEqual(model_dict["updated_at"],
                         model.updated_at.strftime(format))

    def test_str(self):
        """String method validation."""
        instance = BaseModel()
        expected_str = f"[BaseModel] ({instance.id}) {instance.__dict__}"
        self.assertEqual(str(instance), expected_str)

    @mock.patch('models.storage')
    def test_save(self, mocked_storage):
        """Save method test."""
        instance = BaseModel()
        old_created_at = instance.created_at
        old_updated_at = instance.updated_at
        instance.save()
        self.assertNotEqual(old_updated_at, instance.updated_at)
        self.assertEqual(old_created_at, instance.created_at)
        mocked_storage.new.assert_called()
        mocked_storage.save.assert_called()
