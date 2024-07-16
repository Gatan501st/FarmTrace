from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import BaseModel, Role


class User(BaseModel, UserMixin, db.Model):
    __tablename__ = 'users'

    firstname = Column(String(64))
    lastname = Column(String(64))
    company_name = Column(String(64))
    email = Column(String(64), nullable=False, unique=True)
    password_hash = Column(String(128))
    confirmed = Column(Boolean, default=False)
    confirmed_on = Column(DateTime)
    phone = Column(String(64))

    address = Column(String(64))
    city = Column(String(64))
    state = Column(String(64))
    zipcode = Column(String(64))

    two_factor = Column(Boolean)
    sms_notifications = Column(Boolean)
    email_notifications = Column(Boolean)

    role_title = Column(String(64), ForeignKey('roles.title'))
    role = relationship('Role', back_populates='users')

    inventory = relationship('Inventory', back_populates='user', uselist=False)

    shipments = relationship(
        'Shipment', back_populates='user', primaryjoin="and_(Shipment.user_id==User.id)")

    orders_placed = relationship(
        'Order', back_populates='recipient', primaryjoin="and_(Order.recipient_id==User.id)")
    orders_received = relationship('Order', back_populates='sender',
                                   overlaps="orders_placed", primaryjoin="and_(Order.sender_id==User.id)")

    __mapper_args__ = {
        'polymorphic_identity': 'User',
        'polymorphic_on': role_title
    }

    @property
    def password(self):
        raise AttributeError('Cannot access password')

    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)
