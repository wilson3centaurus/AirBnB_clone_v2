#!/usr/bin/python3
'''
    Module for User class
'''
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    '''
        Class User that inherits from BaseModel and Base
    '''
    __tablename__ = 'users'

    # Class attributes
    email = Column(String(128),
                   nullable=False)

    password = Column(String(128),
                      nullable=False)

    first_name = Column(String(128))

    last_name = Column(String(128))

    # Relationships
    if getenv("HBNB_TYPE_STORAGE") == "db":
        places = relationship('Place',
                              backref='user',
                              cascade='all, delete')

        reviews = relationship("Review",
                               backref='user',
                               cascade="all, delete")
