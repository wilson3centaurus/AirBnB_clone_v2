#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
import hashlib
from sqlalchemy import Column, String
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

        """
        @property
        def password(self):
            getter for password
            return self._password

        @password.setter
        def password(self, value):
             Setter for password
            self._password = hashlib.md5(value.encode()).hexdigest()
        """

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        """
        self.password = hashlib.md5(kwargs['password'].encode()).hexdigest()
        """
