from sqlalchemy import Column, String, DateTime
from uuid import uuid4
from datetime import datetime

from app import db

class BaseModel:
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        for key, val in kwargs.items():
            setattr(self, key, val)
        db.session.add(self)

    @property
    def _created_at(self):
        return self.created_at.strftime('%d %B %Y')

    def save(self):
        self.updated_at = datetime.now()
        db.session.commit()

    def delete(self):
        """Deletes an object from the database
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, key, val):
        return db.session.query(cls).filter(getattr(cls, key) == val).first()