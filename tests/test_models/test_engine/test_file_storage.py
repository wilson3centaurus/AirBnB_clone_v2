import unittest
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.state import State
from datetime import datetime
import os


class TestFileStorage(unittest.TestCase):
    """Test cases for the FileStorage class."""

    def setUp(self):
        """Set up for test methods."""
        self.file_path = "file.json"
        self.storage = FileStorage()

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_all(self):
        """Test the all() method."""
        # Initially, all() should return an empty dictionary
        self.assertEqual(self.storage.all(), {})

        # Create a new BaseModel instance and save it to storage
        obj = BaseModel()
        obj.save()

        # After saving, all() should contain one entry
        self.assertEqual(len(self.storage.all()), 1)

        # The entry should be a dictionary with key "BaseModel.<obj_id>"
        key = "BaseModel." + obj.id
        self.assertIn(key, self.storage.all())

        # The value should be the object itself
        self.assertEqual(self.storage.all()[key], obj)

    def test_new(self):
        """Test the new() method."""
        # Create a new State instance and use new() to add it to storage
        state = State(name="California")
        self.storage.new(state)

        # After calling new(), the object should be in the storage dictionary
        key = "State." + state.id
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key], state)

    def test_save_reload(self):
        """Test the save() and reload() methods."""
        # Create a new State instance and save it
        state = State(name="California")
        self.storage.new(state)
        self.storage.save()

        # After saving, clear the storage and reload from file
        self.storage.__objects = {}
        self.storage.reload()

        # After reloading, the State object should be present in all()
        key = "State." + state.id
        self.assertIn(key, self.storage.all())
        self.assertIsInstance(self.storage.all()[key], State)
        self.assertEqual(self.storage.all()[key].name, "California")

    def test_delete(self):
        """Test the delete() method."""
        # Create a new State instance and add it to storage
        state = State(name="California")
        self.storage.new(state)
        self.storage.save()

        # Delete the State instance from storage
        self.storage.delete(state)

        # After deleting, the State object should not be in all()
        key = "State." + state.id
        self.assertNotIn(key, self.storage.all())


if __name__ == "__main__":
    unittest.main()
