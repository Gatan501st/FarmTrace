from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey

from app.models import User
from app import db

class Manufacturer(User):
    __tablename__ = 'manufacturers'
    id = Column(String(64), ForeignKey('users.id'), primary_key=True)
    company_name = Column(String(64), nullable=False)
    registration_date = Column(String(64))
    staff_num = Column(Integer)

    products = relationship('Product', back_populates='manufacturer')

    __mapper_args__ = {
        'polymorphic_identity': 'manufacturer'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = "Manufacturer"

class Wholesaler(User):
    __tablename__ = 'wholesalers'
    id = Column(String(64), ForeignKey('users.id'), primary_key=True)
    company = Column(String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'wholesaler'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = "Wholesaler"

class Retailer(User):
    __tablename__ = 'retailers'
    id = Column(String(64), ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'retailer'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = "Retailer"
