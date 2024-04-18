#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import unittest
from models.engine.db_storage import DBStorage
from models.state import State
from datetime import datetime
import inspect
import models
import json
import os
import pep8

DBStorage = models.storage.__class__


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_db_storage_get_method(self):
        """Test get method in DBStorage"""
        storage = DBStorage()
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()
        retrieved_state = storage.get(State, new_state.id)
        self.assertEqual(retrieved_state, new_state)

    def test_db_storage_count_method(self):
        """Test count method in DBStorage"""
        storage = DBStorage()
        initial_count = storage.count(State)
        new_state1 = State(name="New York")
        new_state2 = State(name="Texas")
        storage.new(new_state1)
        storage.new(new_state2)
        storage.save()
        updated_count = storage.count(State)
        self.assertEqual(updated_count, initial_count + 2)


if __name__ == "__main__":
    unittest.main()
