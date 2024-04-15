#!/usr/bin/python3
"""DBStorage testing."""

import unittest
import pycodestyle
import inspect
from models.engine import db_storage
from models.state import State
from models import storage

DBStorage = db_storage.DBStorage
model_classes = {"Amenity": Amenity, "City": City, "Place": Place,
                 "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """DBStorage documentation tests."""

    @classmethod
    def setUpClass(cls):
        """Prepare doc tests."""
        cls.methods = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance(self):
        """PEP8 style checks."""
        style = pycodestyle.StyleGuide(quiet=True)
        engine_result = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(engine_result.total_errors, 0, "PEP8 errors found.")

    def test_module_doc(self):
        """Module docstring check."""
        self.assertTrue(len(db_storage.__doc__) >= 1)

    def test_class_doc(self):
        """Class docstring check."""
        self.assertTrue(len(DBStorage.__doc__) >= 1)

    def test_method_docs(self):
        """Method docstring checks."""
        for method_name, method in self.methods:
            self.assertTrue(len(method.__doc__) >= 1,
                            f"{method_name} needs a docstring")

    def test_get_method(self):
        """'get' method test."""
        state_id = self.state.id
        state_obj = storage.get(State, state_id)
        self.assertEqual(state_obj, self.state)

    def test_count_method(self):
        """'count' method test."""
        initial_count = len(storage.all())
        new_state = State()
        new_state.save()
        new_count = storage.count()
        self.assertEqual(new_count, initial_count + 1)


class TestDBStorage(unittest.TestCase):
    """DBStorage class tests."""

    @unittest.skipIf(getattr(models, 'storage_type') != 'db', "Skip if not DB")
    def test_all_return_type(self):
        """'all' return type check."""
        self.assertIsInstance(models.storage.all(), dict)

    def test_all_no_class(self):
        """'all' without class test."""

    def test_new_method(self):
        """'new' method test."""

    def test_save_method(self):
        """'save' method test."""
