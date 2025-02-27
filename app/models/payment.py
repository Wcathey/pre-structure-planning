from .db import db, environment, SCHEMA, add_prefix_for_prod
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Payment(db.Model):
    __tablename__ = 'payments'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, ForeignKey(add_prefix_for_prod('assignments.id')), nullable=False)
    client_id = db.Column(db.Integer, ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    preserver_id = db.Column(db.Integer, ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default='Pending') # Pending, Completed, Failed
    payment_method = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    #Relationships
    assignment = relationship('Assignment', back_populates='payments', lazy=True)
    client = relationship('User', foreign_keys=[client_id], back_populates='client_payments')
    preserver = relationship('User', foreign_keys=[preserver_id], back_populates='preserver_payments')

    def to_dict(self):
        return {
            'id': self.id,
            'assignment_id': self.assignment_id,
            'client_id': self.client_id,
            'preserver_id': self.preserver_id,
            'amount': self.amount,
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'created_at': self.created_at,
            'updated_at': self.updated_at


        }
