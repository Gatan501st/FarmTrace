from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Integer, Enum

from app import db
from app.models import BaseModel

class Listing(BaseModel, db.Model):
    __tablename__ = 'listings'
    product_name = Column(String(64))
    avatar_path = Column(String(128))
    description = Column(String(128))
    price = Column(Integer)
    min_order = Column(Integer)
    available_stock = Column(Integer)
    unit_measure = Column(Enum(('tonne', 'kg', 'g', 'l', 'ml', 'pcs')))

    inventory_id = Column(String(64), ForeignKey('inventories.id'))
    inventory = relationship('Inventory', back_populates='listings')

    product_id = Column(String(64), ForeignKey('products.id'))
    product = relationship('Product', back_populates='listings')

    orders = relationship('Order', back_populates='listing')