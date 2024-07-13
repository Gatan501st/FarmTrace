import json, datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app import db
from app.models.base_model import BaseModel


class Shipment(BaseModel, db.Model):
    __tablename__ = 'shipments'
    checkpoints = Column(JSON)
    # Dispatched, In Transit, Delivered
    status = Column(String(16), nullable=False, default='Processing')
    destination = Column(String(64), nullable=False)

    orders = relationship('Order', back_populates='shipment',
                          cascade='all, delete-orphan')

    user_id = Column(String(64), ForeignKey('users.id'))
    user = relationship(
        'User', back_populates='shipments', foreign_keys=[user_id])

    def update_checkpoint(self, location, status):
        checkpoints = json.loads(self.checkpoints)
        checkpoints.append({
            'location': location,
            'date': f'{datetime.datetime.now()}',
            'statuus': status
        })
        self.checkpoints = json.dumps(checkpoints)

    @property
    def get_checkpoints(self):
        return json.loads(self.checkpoints)
