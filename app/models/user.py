from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
import random

from app import db
from app.models import BaseModel
from app.models import Role

class User(BaseModel, UserMixin, db.Model):
    __tablename__ = 'users'
    firstname = Column(String(64))
    lastname = Column(String(64))
    email = Column(String(64), nullable=False)
    username = Column(String(64), index=True)
    password_hash = Column(String(128))
    confirmed = Column(Boolean, default=False)
    confirmed_on = Column(DateTime)

    role_id = Column(String(64), ForeignKey('roles.id'))
    role = relationship('Role', back_populates='users')
    
    def __init__(self, *args, **kwargs) -> None:
        super(User, self).__init__(**kwargs)
        self.generate_username()
        if self.role is None:
            if self.email.split('@')[1] == current_app.config['ORGANIZATION_DOMAIN']:
                self.role = Role.query.filter_by(title='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def generate_username(self):
        fullname = f'{self.firstname} {self.lastname}'
        name_parts = fullname.split()
        
        # Choose a random part of the name to construct the username
        if len(name_parts) > 1:
            # Randomly select parts of the name
            random.shuffle(name_parts)
            generated = ''.join(name_parts[:random.randint(1, len(name_parts))])
        else:
            # If only one part, use it as is
            generated = name_parts[0]
        generated.lower()
        generated += f'{random.randint(10, 999)}'
        if User.get('username', generated) is not None:
            self.generate_username()
        self.username = generated

    @property
    def password(self):
        raise AttributeError('Cannot access password')
    
    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)
    
    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)