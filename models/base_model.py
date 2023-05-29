#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
from os import getenv

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        for key, value in kwargs.items():
            if key == '__class__':
                continue
            setattr(self, key, value)
            if type(self.created_at) is str:
                self.created_at = datetime.strptime(self.created_at, time)
            if type(self.updated_at) is str:
                self.updated_at = datetime.strptime(self.updated_at, time)

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, secure_pwd=True):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
<<<<<<< HEAD
        if secure_pwd:
            if 'password' in new_dict:
                del new_dict['password']
=======
        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        class_name = ''
        if 'self' in frame.f_locals:
            class_name = frame.f_locals["self"].__class__.__name__
        is_fs_writing = func_name == 'save' and class_name == 'FileStorage'
        if 'password' in new_dict and not is_fs_writing:
            del new_dict['password']
>>>>>>> 778ea08ab0a36aadb0a62f27b5459c789b64051d
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)

