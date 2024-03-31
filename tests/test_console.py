#!/usr/bin/python3
''' Test suite for the console'''


import sys
import models
import unittest
from models import storage
from models import State
from models.engine.db_storage import DBStorage
from io import StringIO
from console import HBNBCommand
from unittest.mock import create_autospec
from os import getenv

db = getenv("HBNB_TYPE_STORAGE", "fs")


class test_console(unittest.TestCase):
    ''' Test the console module'''
    def setUp(self):
        '''setup for'''
        self.backup = sys.stdout
        self.capt_out = StringIO()
        sys.stdout = self.capt_out

    def tearDown(self):
    """ Restore the original sys.stdout after each test. """
    sys.stdout = self.backup


    def create(self):
        ''' create an instance of the HBNBCommand class'''
        return HBNBCommand()

    def test_quit(self):
        ''' Test quit exists'''
        console = self.create()
        self.assertTrue(console.onecmd("quit"))

    def test_EOF(self):
    """ Test if the console handles the EOF (End-of-File) command correctly. """
    console = self.create()
    self.assertTrue(console.onecmd("EOF"))


    def test_all(self):
    """ Test if the output of the 'all' command is of type string. """
    console = self.create()
    console.onecmd("all")
    self.assertTrue(isinstance(self.capt_out.getvalue(), str))


    @unittest.skipIf(db == "db", "Testing database storage only")
    def test_show(self):
    """ Test if the output of 'show' command is of type string. """
    console = self.create()
    console.onecmd("create User")
    user_id = self.capt_out.getvalue()
    sys.stdout = self.backup
    self.capt_out.close()
    self.capt_out = StringIO()
    sys.stdout = self.capt_out
    console.onecmd("show User " + user_id)
    x = (self.capt_out.getvalue())
    sys.stdout = self.backup
    self.assertTrue(str is type(x))


   @unittest.skipIf(db == "db", "Testing database storage only")
    def test_show_class_name(self):
    """ Test the error message when the class name is missing for show command. """
    console = self.create()
    console.onecmd("create User")
    user_id = self.capt_out.getvalue()
    sys.stdout = self.backup
    self.capt_out.close()
    self.capt_out = StringIO()
    sys.stdout = self.capt_out
    console.onecmd("show")
    x = (self.capt_out.getvalue())
    sys.stdout = self.backup
    self.assertEqual("** class name missing **\n", x)


    def test_show_class_name(self):
    """ Test the show message error for missing instance id. """
    console = self.create()
    console.onecmd("create User")
    user_id = self.capt_out.getvalue()
    sys.stdout = self.backup
    self.capt_out.close()
    self.capt_out = StringIO()
    sys.stdout = self.capt_out
    console.onecmd("show User")
    x = (self.capt_out.getvalue())
    sys.stdout = self.backup
    self.assertEqual("** instance id missing **\n", x)

    @unittest.skipIf(db == "db", "Testing database storage only")
def test_show_no_instance_found(self):
        """ Test if an appropriate error message is shown when no instance is found. """
        console = self.create()
        console.onecmd("create User")
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        console.onecmd("show User " + "124356876")
        x = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertEqual("** no instance found **\n", x)

    def test_create(self):
        """ Test creating an object using the create method. """
        console = self.create()
        console.onecmd("create User email=adriel@hbnb.com password=abc")
        self.assertTrue(isinstance(self.capt_out.getvalue(), str))

    def test_class_name(self):
        """ Test if an appropriate error message is shown when the class name is missing. """
        console = self.create()
        console.onecmd("create")
        x = (self.capt_out.getvalue())
        self.assertEqual("** class name missing **\n", x)


class TestClassNameDoesNotExist(unittest.TestCase):
    """ Test case for ensuring error message when class doesn't exist. """

    def test_class_name_does_not_exist(self):
        """ Test if an appropriate error message is shown when the class doesn't exist. """
        console = self.create()
        console.onecmd("create Binita")
        x = (self.capt_out.getvalue())
        self.assertEqual("** class doesn't exist **\n", x)

    @unittest.skipIf(db != 'db', "Testing DBstorage only")
    def test_create_db(self):
        """Test creating an object in the database storage."""
        console = self.create()
        console.onecmd("create State name=California")
        result = storage.all("State")
        self.assertTrue(len(result) > 0)

