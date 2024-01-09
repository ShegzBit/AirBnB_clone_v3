#!/usr/bin/python3
""" holds class User"""
import sqlalchemy
from hashlib import md5
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import models
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    @staticmethod
    def hash_password(password):
        """Hashes the input password using MD5"""
        md5_hash = md5()
        md5_hash.update(password.encode('utf-8'))
        return md5_hash.hexdigest()

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        if self.password is not None:
            self.password = self.hash_password(self.password)
