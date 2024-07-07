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
    email = Column(String(64), nullable=False, unique=True)
    password_hash = Column(String(128))
    confirmed = Column(Boolean, default=False)
    confirmed_on = Column(DateTime)
    location = Column(String(64))

    role_title = Column(String(64), ForeignKey('roles.title'))
    role = relationship('Role', back_populates='users')

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
