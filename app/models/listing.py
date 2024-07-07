from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Integer

from app import db
from app.models import BaseModel

class Listing(BaseModel, db.Model):
    __tablename__ = 'listings'
    price = Column(Integer)
    min_order = Column(Integer)
    available_stock = Column(Integer)

    user = relationship('User', back_populates='listings')
    user_id = Column(String(64), ForeignKey('users.id'))