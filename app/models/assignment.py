
from .db import db, environment, SCHEMA, add_prefix_for_prod
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum

class AssignmentStatus(PyEnum):
    PENDING = "Pending"#Client submits assignment
    FUNDED = "Funded"   # Client pays and charge is cleared/ hold placed to cover expense
    OPEN = "Open"   # Admin verifies payment, assignment pushed to market
    ASSIGNED = "Assigned" # Perserver can now view assignment and claim
    STARTED = "Started" # Perserver arrives and is scanning documents
    SUBMITTED = "Submitted"  # Perserver completes all scans and goes into review
    COMPLETED = "Completed" # Admin confirms completion and marks complete
    CANCELLED = "Cancelled" # Assignment can be canceled due to many reasons by all parties for different reasons
    PAID_OUT = "Paid_Out" # After completion All statuses have been covered and funds can be issued to preserver


class Assignment(db.Model):
    __tablename__ = 'assignments'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    preserver_id = db.Column(db.Integer, ForeignKey(add_prefix_for_prod('preservers.id')), nullable=True)  # Can be NULL initially
    description = db.Column(db.String(255), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    location_id = db.Column(db.Integer, ForeignKey(('locations.id')), nullable=False)
    status = db.Column(db.Enum(AssignmentStatus), default=AssignmentStatus.PENDING)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now()) #posted date
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now())

    #Relationships
    client = relationship('User', foreign_keys=[client_id])
    preserver = relationship('Preserver', back_populates='assignments') #One Preserver per Assignment
    location = relationship('Location', back_populates='assignments')
    payments = relationship('Payment', back_populates='assignment', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'base_price': self.base_price,
            'location_id': self.location_id,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'client': self.client.to_dict(),  # Assuming 'User' model has a to_dict method
            'preserver': self.preserver.to_dict() if self.preserver else None,
            'location': self.location.to_dict()  # Assuming 'Location' model has a to_dict method
        }
