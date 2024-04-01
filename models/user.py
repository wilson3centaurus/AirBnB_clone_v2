#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
import hashlib
from sqlalchemy import Column, String, event
import hashlib
from models.base_model import BaseModel, Base
import models
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship(
                "Place",
                backref="user",
                cascade='all, delete, delete-orphan')
        reviews = relationship(
                "Review",
                backref="user",
                cascade='all, delete, delete-orphan')
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

        @property
        def password(self):
            """ getter for password """
            return self.password

        @password.setter
        def password(self, value):
            """ Setter for password """

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)


def hash_password_before_insert_or_update(_, __, target):
    if target.password is not None:
        # Hash the password using MD5
        target.password = hashlib.md5(target.password.encode()).hexdigest()


event.listen(User, 'before_insert', hash_password_before_insert_or_update)
event.listen(User, 'before_update', hash_password_before_insert_or_update)
