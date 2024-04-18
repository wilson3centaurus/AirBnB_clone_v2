#!/usr/bin/python3
'''
    Module for City class

'''
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    '''
        Class City that inherits from BaseModel and Base
    '''
    __tablename__ = 'cities'

    # Class attributes
    name = Column(String(128),
                  nullable=False)

    state_id = Column(String(60),
                      ForeignKey('states.id'),
                      nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        # Relationship with State
        places = relationship('Place',
                              backref='cities',
                              cascade='all, delete')
