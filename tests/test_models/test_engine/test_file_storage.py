import unittest
from models.engine.file_storage import FileStorage
from models.state import State
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

    def test_file_storage_get_method(self):
        """Test get method in FileStorage"""
        storage = FileStorage()
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()
        retrieved_state = storage.get(State, new_state.id)
        self.assertEqual(retrieved_state, new_state)

    def test_file_storage_count_method(self):
        """Test count method in FileStorage"""
        storage = FileStorage()
        initial_count = storage.count(State)
        new_state1 = State(name="New York")
        new_state2 = State(name="Texas")
        storage.new(new_state1)
        storage.new(new_state2)
        storage.save()
        updated_count = storage.count(State)
        self.assertEqual(updated_count, initial_count + 2)

    def test_file_storage_all_method(self):
        """Test all method in FileStorage"""
        storage = FileStorage()
        new_state = State(name="Florida")
        storage.new(new_state)
        storage.save()
        all_objects = storage.all()
        self.assertIn(
            type(new_state).__name__ + '.' + new_state.id, all_objects)

    def test_file_storage_new_method(self):
        """Test new method in FileStorage"""
        storage = FileStorage()
        new_state = State(name="Arizona")
        storage.new(new_state)
        self.assertIn(
            type(new_state).__name__ + '.' + new_state.id, storage.all())

    def test_file_storage_save_reload_integration(self):
        """Test save and reload methods in FileStorage"""
        storage = FileStorage()
        new_state = State(name="Oregon")
        storage.new(new_state)
        storage.save()

        new_storage = FileStorage()
        new_storage.reload()
        retrieved_state = new_storage.get(State, new_state.id)

        self.assertIsNotNone(retrieved_state)
        self.assertEqual(retrieved_state.name, "Oregon")

    def test_file_storage_delete_method(self):
        """Test delete method in FileStorage"""
        storage = FileStorage()
        new_state = State(name="Washington")
        storage.new(new_state)
        storage.save()

        storage.delete(new_state)
        self.assertIsNone(storage.get(State, new_state.id))
        self.assertNotIn(
            type(new_state).__name__ + '.' + new_state.id, storage.all())


if __name__ == "__main__":
    unittest.main()
