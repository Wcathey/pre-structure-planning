from .db import db, environment, SCHEMA, add_prefix_for_prod
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Review(db.Model):
    __tablename__ = 'reviews'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, ForeignKey(add_prefix_for_prod('assignments.id')), nullable=False)
    reviewer_id = db.Column(db.Integer, ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    reviewee_id = db.Column(db.Integer, ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    rating = db.Column(db.Integer, nullable=False) #1-5 star rating
    comment = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    #Relationships
    assignment = relationship('Assignment', back_populates='assignments')
    reviewer = relationship('User', foreign_keys=[reviewer_id], backref='reviews_given')
    reviewee = relationship('User', foreign_keys=[reviewee_id], backref='reviews_received')


    def to_dict(self):
        return {
            'id': self.id,
            'assignment_id': self.assignment_id,
            'reviewer_id': self.reviewer_id,
            'reviewee_id': self.reviewee_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at,
            'updated_at': self.updated_at,

        }
