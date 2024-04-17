#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for key in classes:
            db_cls = classes[key]
            if cls is None or cls is db_cls or cls is key:
                objs = self.__session.query(db_cls).all()
                for obj_value in objs:
                    id = obj_value.id
                    obj_key = obj_value.__class__.__name__ + '.' + id
                    new_dict[obj_key] = obj_value
        return (new_dict)

    def get(self, cls, id):
        """
            Search for an object of type 'cls' and with id 'id' in storage.
            If found return it, else return nothing.
        """
        # Search in the objects in storage for object with cls, id
        try:
            return self.__session.query(classes[cls.__name__]).get(id)
        except Exception:
            return None

    def count(self, cls=None):
        """
            Returns the number of objects in storage that matches the
            given class. If none are passed, return the count of all objects
            in storage
        """
        try:
            if (cls is None):
                return len(self.all())
            else:
                classe = classes[cls.__name__]
                return len(self.all(classe))
        except Exception:
            return None

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
