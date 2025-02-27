from .db import db, environment, SCHEMA, add_prefix_for_prod
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Location(db.Model):
    __tablename__ = 'locations'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    optional_address_ext = db.Column(db.String(50)) #suite, unit, apt,
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zipcode =db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    #Relationships
    assignments = relationship('Assignment', back_populates="location", lazy=True)




    def to_dict(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude':self.longitude,
            'address': self.address,
            'optional_address_ext': self.optional_address_ext,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
