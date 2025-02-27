from .db import db, environment, SCHEMA, add_prefix_for_prod
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func




class Availability(db.Model):
    __tablename__ = 'availabilities'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    sunday = db.Column(db.String(10), nullable=False, default="Open")
    monday = db.Column(db.String(10), nullable=False, default="Open")
    tuesday = db.Column(db.String(10), nullable=False, default="Open")
    wednesday = db.Column(db.String(10), nullable=False, default="Open")
    thursday = db.Column(db.String(10), nullable=False, default="Open")
    friday = db.Column(db.String(10), nullable=False, default="Open")
    saturday = db.Column(db.String(10), nullable=False, default="Open")
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    #Relationships
    user = relationship('User', back_populates='availability')


    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'sunday': self.sunday,
            'monday': self.monday,
            'tuesday': self.tuesday,
            'wednesday': self.wednesday,
            'thursday': self.thursday,
            'friday': self.friday,
            'saturday': self.saturday,
            'created_at': self.created_at,
            'updated_at': self.updated_at

        }
