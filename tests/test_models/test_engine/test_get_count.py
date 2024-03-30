#!/usr/bin/python3
import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

"""Test .get() and .count() methods"""

from models import storage
from models.state import State


class TestGetCountMethods(unittest.TestCase):
    """Test .get() and .count() methods"""

    def test_get_method(self):
        """Test the .get() method"""
        print("All objects: {}".format(storage.count()))
        print("State objects: {}".format(storage.count(State)))

    def test_count_method(self):
        """Test the .count() method"""
        first_state_id = list(storage.all(State).values())[0].id
        print("First state: {}".format(storage.get(State, first_state_id)))

if __name__ == '__main__':
    unittest.main()
