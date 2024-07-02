from datetime import datetime

from app import db

class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_number = db.Column(db.String(64), unique=True, nullable=False)
    type = db.Column(db.String(64), nullable=False)
    composition = db.Column(db.String(128), nullable=False)
    production_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    expiry_date = db.Column(db.DateTime, nullable=False)
    manufacturer_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )
