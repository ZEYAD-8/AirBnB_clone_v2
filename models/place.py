#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from models.city import City
from models.review import Review

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
import models.engine


place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id",
                             String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id",
                             String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ Represents a Place for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table places
    """
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

    reviews = relationship("Review",
                           backref="place",
                           cascade="all, delete, delete-orphan")

    amenities = relationship("Amenity",
                             secondary=place_amenity,
                             back_populates="place_amenities",
                             viewonly=False)

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

        @property
        def amenities(self):
            """ Get/set linked Amenities."""
            from models.amenity import Amenity
            amenity_list = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            from models.amenity import Amenity
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
