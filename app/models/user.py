from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Enum
from enum import Enum as PyEnum #avoid confict with SQLAlchemy's Enum

class UserType(PyEnum):
    CLIENT = "Client"
    PRESERVER = "Preserver"

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(Enum(UserType, native_enum=False), nullable=False) #Client or Preserver
    rating = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    #Relationships
    reviews_given = relationship('Review', foreign_keys=["Review.reviewer_id"], backref="reviewer", lazy=True)
    reviews_recieved = relationship('Review', foreign_keys=["Review.reviewee_id"], backref="reviewee", lazy=True)
    availability = relationship('Availability', uselist=False, back_populates='user')
    client_payments = relationship('Payment', foreign_keys=["Payment.client_id"], back_populates="client")
    preserver_payments = relationship('Payment', foreign_keys=["Payment.preserver_id"], back_populates="preserver")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
            'user_type': self.user_type.value,
            'rating': self.rating,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
