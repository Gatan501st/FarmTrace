import qrcode
from flask import current_app
from app import db
from app.models import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Text, ForeignKey, JSON, DateTime, Integer

class Product(BaseModel, db.Model):
    __tablename__ = 'products'
    name = Column(String(25), nullable=False)
    description = Column(Text, nullable=False)

    batches = relationship('Batch', back_populates='product')
    manufacturer_id = Column(String(64), ForeignKey('manufacturers.id'))
    manufacturer = relationship('Manufacturer', back_populates='products')
    
    listings = relationship('Listing', back_populates='product')

    orders = relationship('Order', back_populates='product')

    def generate_qrcode(self):
        """
        Generate QR Code for a product
        """
        data = {
            "product_id": self.id,
            "product_name": self.name,
            "batch_number": self.batch_id,
            "manufacture_date": self.manufacturer_date,
            "expiry_date": self.expiry_date,
            "manufacturer_name": self.manufacturer.fullname,
            "manufacturing_location": self.manufacturer.company_location,
            "checkpoints": [],
            "auth_url": f"{current_app.config['HOST']}/product/verify?product_id={self.id}",
            "digital_signature": "abcd1234efgh5678ijkl"
		}
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save()

    def update_checkpoint(self):
        pass