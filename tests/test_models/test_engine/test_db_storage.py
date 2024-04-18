#!/usr/bin/python3
"""Module contains tests for DBStorage class"""

from os import getenv
from models.engine.db_storage import DBStorage
from models.review import Review
from models.place import Place
from models.user import User
from models.state import State
from models.city import City
import unittest
from models.base_model import BaseModel
import MySQLdb

storage = DBStorage()
storage_engine = getenv("HBNB_TYPE_STORAGE")

mydb = MySQLdb.connect(
    host=getenv("HBNB_MYSQL_HOST"),
    user=getenv("HBNB_MYSQL_USER"),
    password=getenv("HBNB_MYSQL_PWD"),
    database=getenv("HBNB_MYSQL_DB")
)


@unittest.skipIf(storage_engine != "db", "db storage is not being used")
class test_dbStorage(unittest.TestCase):
    """Class that tests DBStorage methods"""

    @classmethod
    def setUpClass(cls):
        """
        Connect to the database before all tests
        """
        cls.mydb = MySQLdb.connect(
            host=getenv("HBNB_MYSQL_HOST"),
            user=getenv("HBNB_MYSQL_USER"),
            password=getenv("HBNB_MYSQL_PWD"),
            database=getenv("HBNB_MYSQL_DB")
        )
        cls.mycursor = cls.mydb.cursor()

    @classmethod
    def tearDownClass(cls):
        """
        Close the database connection after all tests
        """
        cls.mycursor.close()
        cls.mydb.close()

    def setUp(self):
        """Setup test environment"""
        mycursor = self.mycursor
        mycursor.execute("DELETE FROM states")
        self.mydb.commit()

        self.db = DBStorage()
        self.db.reload()

    def tearDown(self):
        self.db.reload()

    def test_init(self):
        """test_dbStorage Init method"""
        self.assertTrue(self.db._DBStorage__engine is not None)
        self.assertTrue(self.db._DBStorage__session is not None)

    def test_new(self):
        """Test DBStorage.new method"""
        new_state = State(name="California")
        self.db.new(new_state)
        self.db.save()

        mycursor = self.mycursor
        mycursor.execute(
            "SELECT * FROM states WHERE name = %s", ("California",))
        result = mycursor.fetchone()
        self.assertEqual(result[0], "California")

    def test_save(self):
        """Test DBStorage.save method"""
        new_state = State(name="Texas")
        self.db.new(new_state)
        self.db.save()

        mycursor = self.mycursor
        mycursor.execute("SELECT * FROM states WHERE name = %s", ("Texas",))
        result = mycursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Texas")

    def test_delete(self):
        "Test DBStorage.delete method"
        new_state = State(name="California")
        self.db.new(new_state)
        self.db.save()
        mycursor = self.mycursor
        mycursor.execute(
            "SELECT * FROM states WHERE name = %s", ("California",))
        result = mycursor.fetchone()
        self.assertEqual(result[0], "California")

        self.db.delete(new_state)
        self.db.save()
        all_states = self.db.all(State)
        california_state = all_states.get(f"{State.__name__}.{new_state.id}")

        self.assertIsNone(california_state)

    def test_delete_none(self):
        """Test DBStorage.delete method with no argument"""
        new_state = State(name="California")
        self.db.new(new_state)
        self.db.save()
        all_objs_before = self.db.all()
        self.db.delete()
        self.db.save()
        all_states = self.db.all(State)
        california_state = all_states.get(f"{State.__name__}.{new_state.id}")

        self.assertIsNotNone(california_state)

    def test_reload(self):
        """Test DBStorage.reload method"""
        new_state = State(name="California")
        self.db.new(new_state)
        self.db.save()
        self.db.reload()
        key = f"{type(new_state).__name__}.{new_state.id}"
        self.assertIn(key, self.db.all())

    def test_all(self):
        """Test DBStorage.all method"""
        obj_dict = self.db.all()
        self.assertIsInstance(obj_dict, dict)
        for val in obj_dict.values():
            self.assertIsInstance(val, BaseModel)

    def test_all_with_classes(self):
        """Test DBStorage.all method with class argument"""
        obj_dict = self.db.all(State)
        self.assertIsInstance(obj_dict, dict)
        for val in obj_dict.values():
            self.assertIsInstance(val, State)

    def test_get_method(self):
        """Test get method with class argument"""
        state_obj = State(name='test')
        state_id = state_obj.id
        self.db.new(state_obj)
        self.db.save()
        retrieved_state = self.db.get(State, state_id)

        self.assertEqual(state_id, retrieved_state.id)
        fake_id = '12243'
        retrieved_state = self.db.get(State, fake_id)
        self.assertEqual(retrieved_state, None)

    def test_count_method(self):
        """Test get method with class argument"""
        all_states = self.db.all(State)
        state_count = self.db.count(State)
        self.assertEqual(len(all_states), state_count)

        all_obj = self.db.all()
        all_count = self.db.count()
        self.assertEqual(len(all_obj), all_count)


if __name__ == "__main__":
    unittest.main()
