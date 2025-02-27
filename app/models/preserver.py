from .db import db, environment, SCHEMA, add_prefix_for_prod
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Preserver(db.Model):
    __tablename__ = 'preservers'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, ForeignKey(add_prefix_for_prod('users.id')), primary_key=True)
    availability_id = db.Column(db.Integer, ForeignKey(add_prefix_for_prod('availabilities.id')), nullable=False)
    clearance = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    #Relationships
    availability = relationship('Availability', backref="preservers", uselist=False)  # One-to-One
    assignments = relationship('Assignment', back_populates='preserver', uselist=False)  # One-to-One
    user = relationship("User", backref="preserver", uselist=False)  # One-to-One relationship with User

    def to_dict(self):
        return {
            'id': self.id,
            'availability_id': self.availability_id,
            'clearance': self.clearance,
            'created_at': self.created_at,
            'updated_at': self.updated_at

        }
