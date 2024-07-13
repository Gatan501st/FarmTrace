from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app import db
from app.models.base_model import BaseModel


class Order(BaseModel, db.Model):
    __tablename__ = 'orders'
    quantity = Column(Integer)
    total_price = Column(Float)
    status = Column(String(64), default='Pending')
    order_date = Column(DateTime)
    delivery_date = Column(DateTime)
    qrcode = Column(String(128))

    items = relationship('Item', back_populates='order')

    payment_method = Column(String(64))
    payment_status = Column(String(64), default='Pending')

    delivery_status = Column(String(64), default='Pending')
    delivery_address = Column(String(128))

    product_id = Column(String(64), ForeignKey('products.id'))
    product = relationship('Product', back_populates='orders')

    sender_id = Column(String(64), ForeignKey('users.id'))
    sender = relationship('User', back_populates='orders_received',
                          overlaps="orders_placed", foreign_keys=[sender_id])

    recipient_id = Column(String(64), ForeignKey('users.id'))
    recipient = relationship('User', back_populates='orders_placed',
                             overlaps="orders_received,sender", foreign_keys=[recipient_id])

    listing_id = Column(String(64), ForeignKey('listings.id'))
    listing = relationship('Listing', back_populates='orders')

    shipment_id = Column(String(64), ForeignKey('shipments.id'))
    shipment = relationship('Shipment', back_populates='orders')

    def __repr__(self):
        return f'<Order {self.id}>'
