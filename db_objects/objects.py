from sqlalchemy import Column, Integer, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import PrimaryKeyConstraint

Base = declarative_base()


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)


class KitchenType(Base):
    __tablename__ = 'kitchen_types'
    id = Column(Integer, primary_key=True)
    type = Column(Text)


class Meal(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    meal = Column(Text)
    kitchen_type_id = Column(Integer, ForeignKey('kitchen_types.id'))

    kitchen_type = relationship('KitchenType')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Text)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    nr_of_reservations = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user_location_id = Column(Integer, ForeignKey('locations.id'))
    kitchen_type_id = Column(Integer, ForeignKey('kitchen_types.id'))

    user = relationship('User')
    user_location = relationship('Location')
    kitchen_type = relationship('KitchenType')


class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    rate = Column(Integer)
    nr_of_tables = Column(Integer)
    kitchen_type_id = Column(Integer, ForeignKey('kitchen_types.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))

    location = relationship('Location')
    kitchen_type = relationship('KitchenType')


class ReservedTables(Base):
    __tablename__ = 'reserved_tables'
    id = Column(Integer, primary_key=True)
    total_nr_of_reservations = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

    restaurant = relationship('Restaurant')
