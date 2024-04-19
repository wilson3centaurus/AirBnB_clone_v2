#!/usr/bin/python3
"""
Contains the TestFileStorageDocs and TestFileStorage classes for unit testing
"""

import unittest 
from models.engine.file_storage import FileStorage
from models.state import State
from models.city import City
from datetime import datetime
import models
import json
import os
import pep8

FileStorage = models.storage.__class__


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")


class TestFileStorage(unittest.TestCase):
    """Tests for the FileStorage class"""

    def setUp(self):
        """Set up test fixtures"""
        self.storage = FileStorage()
        self.state = State(name="California")
        self.city = City(name="San Francisco", state_id=self.state.id)

    def tearDown(self):
        """Tear down test fixtures"""
        self.storage.reload()
        if os.path.exists(self.storage._FileStorage__file_path):
            os.remove(self.storage._FileStorage__file_path)

    def test_new_method(self):
        """Test the new method of FileStorage"""
        self.storage.new(self.state)
        self.assertTrue(
            f"State.{self.state.id}" in self.storage._FileStorage__objects)
        self.storage.new(self.city)
        self.assertTrue(
            f"City.{self.city.id}" in self.storage._FileStorage__objects)

    def test_save_method(self):
        """Test the save method of FileStorage"""
        self.storage.new(self.state)
        self.storage.new(self.city)
        self.storage.save()
        self.assertTrue(os.path.exists(self.storage._FileStorage__file_path))

    def test_reload_method(self):
        """Test the reload method of FileStorage"""
        self.storage.new(self.state)
        self.storage.save()
        self.storage.reload()
        self.assertTrue(
            f"State.{self.state.id}" in self.storage._FileStorage__objects)

    def test_delete_method(self):
        """Test the delete method of FileStorage"""
        self.storage.new(self.state)
        self.storage.save()
        self.storage.delete(self.state)
        self.assertTrue(
            f"State.{self.state.id}" not in self.storage._FileStorage__objects)

    def test_get_method(self):
        """Test the get method of FileStorage"""
        self.storage.new(self.state)
        self.storage.save()
        retrieved_state = self.storage.get(State, self.state.id)
        self.assertEqual(retrieved_state, self.state)

    def test_count_method(self):
        """Test the count method of FileStorage"""
        initial_count = self.storage.count(State)
        self.assertEqual(initial_count, 0)
        self.storage.new(self.state)
        self.storage.new(self.city)
        self.storage.save()
        updated_count = self.storage.count(State)
        self.assertEqual(updated_count, 1)


if __name__ == "__main__":
    unittest.main()
