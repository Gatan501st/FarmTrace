from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey

from app.models import User, Role
from app import db


class Administrator(User):
    __tablename__ = 'admins'
    id = Column(String(64), ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Administrator'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = Role.get('title', 'Administrator')


class Manufacturer(User):
    __tablename__ = 'manufacturers'
    id = Column(String(64), ForeignKey('users.id'), primary_key=True)
    registration_date = Column(String(64))
    staff_num = Column(Integer)

    products = relationship('Product', back_populates='manufacturer')

    __mapper_args__ = {
        'polymorphic_identity': 'Manufacturer'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = Role.get('title', 'Manufacturer')


class Wholesaler(User):
    __tablename__ = 'wholesalers'
    id = Column(String(64), ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Wholesaler'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = Role.get('title', 'Wholesaler')


class Retailer(User):
    __tablename__ = 'retailers'
    id = Column(String(64), ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Retailer'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = Role.get('title', 'Retailer')


class Farmer(User):
    __tablename__ = 'farmers'
    id = Column(String(64), ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Farmer'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = Role.get('title', 'Farmer')
