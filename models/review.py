#!/usr/bin/python3
'''
    Module for Review class
'''
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    '''
        Review class
    '''
    __tablename__ = 'reviews'

    # Class attributes
    text = Column(String(1024),
                  nullable=False)

    place_id = Column(String(60),
                      ForeignKey('places.id'), nullable=False)

    user_id = Column(String(60),
                     ForeignKey('users.id'), nullable=False)
