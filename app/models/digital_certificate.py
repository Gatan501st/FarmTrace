from datetime import datetime

from app import db


class DigitalCertificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey("batch.id"), nullable=False)
    certificate_hash = db.Column(db.String(64), nullable=False)
    issued_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
