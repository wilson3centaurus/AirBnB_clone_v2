#!/usr/bin/python3
"""Tests for FileStorage classes."""

import unittest
import inspect
import models
from models.engine.file_storage import FileStorage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import pycodestyle

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Documentation and PEP8 compliance tests."""

    @classmethod
    def setUpClass(cls):
        """Gather methods for doc tests."""
        cls.funcs = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test code style adherence."""
        style_guide = pycodestyle.StyleGuide(quiet=True)
        result = style_guide.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0, "Found PEP8 issues.")

    def test_module_docs(self):
        """Module docstring existence."""
        self.assertIsNotNone(FileStorage.__doc__, "Missing module docstring.")

    def test_class_docs(self):
        """Class docstring existence."""
        self.assertTrue(len(FileStorage.__doc__) >=
                        1, "Missing class docstring.")

    def test_function_docs(self):
        """Function docstring tests."""
        for func_name, func in self.funcs:
            self.assertIsNotNone(
                func.__doc__, f"{func_name} missing docstring.")


class TestFileStorage(unittest.TestCase):
    """Functional tests for FileStorage."""

    @unittest.skipIf(models.storage_t == 'db', "DB storage not tested.")
    def test_all_returns_dict(self):
        """'all' method returns dict."""
        storage_instance = FileStorage()
        self.assertIsInstance(storage_instance.all(), dict)

    @unittest.skipIf(models.storage_t == 'db', "DB storage not tested.")
    def test_new(self):
        """'new' method functionality."""
        storage_instance = FileStorage()
        initial_objects = FileStorage._FileStorage__objects.copy()
        try:
            for class_name, class_type in classes.items():
                instance = class_type()
                storage_instance.new(instance)
                instance_key = f"{class_name}.{instance.id}"
                self.assertIn(instance_key, storage_instance.all())
        finally:
            FileStorage._FileStorage__objects = initial_objects

    @unittest.skipIf(models.storage_t == 'db', "DB storage not tested.")
    def test_save(self):
        """'save' method functionality."""
        storage_instance = FileStorage()
        initial_objects = FileStorage._FileStorage__objects.copy()
        try:
            test_dict = {}
            for class_name, class_type in classes.items():
                instance = class_type()
                instance_key = f"{class_name}.{instance.id}"
                storage_instance.new(instance)
                test_dict[instance_key] = instance.to_dict()
            storage_instance.save()
            with open("file.json", "r") as file:
                data = json.load(file)
            self.assertEqual(test_dict, data)
        finally:
            FileStorage._FileStorage__objects = initial_objects

    @unittest.skipIf(models.storage_t == 'db', "DB storage not tested.")
    def test_get(self):
        """'get' method tests."""
        storage_instance = FileStorage()
        dic = {"name": "Vecindad"}
        instance = State(**dic)
        storage_instance.new(instance)
        storage_instance.save()
        self.assertEqual(storage_instance.get(State, instance.id), instance)

    @unittest.skipIf(models.storage_t == 'db', "DB storage not tested.")
    def test_count(self):
        """'count' method tests."""
        storage_instance = FileStorage()
        state = State(name="Vecindad")
        city = City(name="Mexico")
        storage_instance.new(state)
        storage_instance.new(city)
        storage_instance.save()
        expected_count = len(storage_instance.all())
        self.assertEqual(storage_instance.count(), expected_count)
