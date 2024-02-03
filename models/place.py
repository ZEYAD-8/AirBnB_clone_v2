#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from models.city import City
from models.review import Review
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
import models.engine

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)

    name = Column(String(128), nullable=False)
    description = Column(String(1024))

    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)

    latitude = Column(Float)
    longitude = Column(Float)

    reviews = relationship("Review", backref="place", cascade="all, delete, delete-orphan")
    # reviews = relationship("Review", backref="place", cascade="delete")
    amenity_ids = []


    if os.environ.get('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """ Get a list of all linked Reviews. """
            place_reviews = []
            reviews_list = list(models.storage.all(Review).values())
            for review in reviews_list:
                if review.place_id == self.id:
                    place_reviews.append(review)
            return place_reviews