#!/usr/bin/python3
'''
    Module for State class
'''
from models.base_model import BaseModel, Base
from models.city import City
import models
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    '''
        Class State that inherits from BaseModel and Base
    '''
    __tablename__ = 'states'

    # Class attributes
    name = Column(String(128),
                  nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City',
                              backref='state',
                              cascade='all, delete')
    else:
        @property
        def cities(self):
            '''
                Getter attribute that returns the list of City instances
                with state_id equals to the current State.id
            '''
            st_cities = []
            for city in models.storage.all(City).values():
                if self.id == city.state_id:
                    st_cities.append(city)

            return st_cities
