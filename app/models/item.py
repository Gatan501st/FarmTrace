from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Integer

from app import db
from app.models import BaseModel

class Item(BaseModel, db.Model):
    __tablename__ = 'items'
    batch_id = Column(String(64), ForeignKey('batches.id'))
    qrcode = Column(String(64))

    batch_id = Column(String(64), ForeignKey('batches.id'))
    batch = relationship('Batch', back_populates='items')

    order_id = Column(String(64), ForeignKey('orders.id'))
    order = relationship('Order', back_populates='items')
