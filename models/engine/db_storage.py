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
        obj_data = {}
        if cls:
              all_obj = self.__session.query(cls).all()
        else:
            all_obj = []
            for cls_name, cls_model in classes.items():
                all_obj.extend(self.__session.query(cls_model).all())
        for i in all_obj:
            obj_ref = "[{}.{}])".format(type(i).__name__, i.id)
            obj_data[obj_ref] = i
        return obj_data

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def get(self, cls, id):
        """returning an objects based on its class and id"""
        if cls and id:
            all_obj = self.all(cls)
            for key, val in all_obj.items():
                if val.id == id:
                    one_obj = {
                        'name': val.name,
                        'id': val.id,
                        'created_at': val.created_at,
                        'updated_at': val.updated_at,
                        '_sa_instance_state': val._sa_instance_state
                    }
                    return ("[{}] ({}) {}".format(cls.__name__, val.id, one_obj))
        return None

    def count(self, cls=None):
        """return the numbero of objects present for given class"""
        if cls is not None:
            all_obj = self.all(cls)
            if cls in all_obj:
                return len(all_obj.get(cls))
        return (len(self.all(cls)))

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
