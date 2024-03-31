#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
<<<<<<< HEAD
        places = relationship("Place", cascade='all, delete, delete-orphan',
                              backref="user")
        reviews = relationship("Review", cascade='all, delete, delete-orphan',
                               backref="user")
=======
        places = relationship(
                "Place",
                backref="user",
                cascade='all, delete, delete-orphan')
        reviews = relationship(
                "Review",
                backref="user",
                cascade='all, delete, delete-orphan')
>>>>>>> c9949bbf03987e284089d5f8740ce6b4e6c8fa44
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
