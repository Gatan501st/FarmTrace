from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer

from app import db
from app.models import BaseModel

class Batch(BaseModel, db.Model):
    __tablename__ = 'batches'
    batch_number = Column(String(25), unique=True)
    qrcode = Column(String(64))
    manufacture_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    size = Column(Integer, nullable=False) # in kgs
    measurement = Column(String(16), nullable=False) #kgs, tonnes, litres, ml, packets, 

    product_id = Column(String(64), ForeignKey('products.id'))
    product = relationship('Product', back_populates='batches')

    items = relationship('Item', back_populates='batch')
