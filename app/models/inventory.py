from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Integer

from app.models import BaseModel, db

class Inventory(BaseModel, db.Model):
    __tablename__ = 'inventories'
    quantity = Column(Integer)
    price = Column(Integer)
    
    item_id = Column(String(64), ForeignKey('items.id'))
    item = relationship('Item', back_populates='inventories')
    
    user_id = Column(String(64), ForeignKey('users.id'))
    user = relationship('User', back_populates='inventories')