#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """A base class for all hbnb models"""
        MySQL_user = os.environ.get("HBNB_MYSQL_USER")
        MySQL_password = os.environ.get("HBNB_MYSQL_PWD")
        MySQL_host = os.environ.get("HBNB_MYSQL_HOST")
        MySQL_database = os.environ.get("HBNB_MYSQL_DB")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(MySQL_user,
                                              MySQL_password,
                                              MySQL_host,
                                              MySQL_database),
                                      pool_pre_ping=True)

        if os.environ.get("HBNB_ENV") == "test":
            # Drop all tables
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """ returns a dictionary
        Return:
            returns a dictionary of __object
        """
        dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for obj in query:
                obj_key = "{}.{}".format(type(obj).__name__, obj.id)
                dic[obj_key] = obj
        else:
            classes = [State, City, User, Place, Review, Amenity]
            for class_name in classes:
                query = self.__session.query(class_name)
                for obj in query:
                    obj_key = "{}.{}".format(type(obj).__name__, obj.id)
                    dic[obj_key] = obj
        return (dic)

    def new(self, obj):
        """ add a new element in the table """
        self.__session.add(obj)

    def save(self):
        """ save changes """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete an element in the table """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ configuration """
        Base.metadata.create_all(self.__engine)
        Session_factory = sessionmaker(bind=self.__engine,
                                       autocommit=False,
                                       expire_on_commit=False)

        Session = scoped_session(Session_factory)
        self.__session = Session()

    def close(self):
        """function that closes current database"""
        self.__session.close()
