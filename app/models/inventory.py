from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Integer

from app.models import BaseModel, db

class Inventory(BaseModel, db.Model):
    __tablename__ = 'inventories'
    name = Column(Integer)
    description = Column(Integer)

    listings = relationship('Listing', back_populates='inventory')

    user_id = Column(String(64), ForeignKey('users.id'))
    user = relationship('User', back_populates='inventory', uselist=False)