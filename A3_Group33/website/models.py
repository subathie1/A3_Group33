from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Relationships
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    orders = db.relationship('Order', backref='order_user', lazy='dynamic')
    bookings = db.relationship('Booking', backref='booking_user', lazy='dynamic')
    events = db.relationship('Event', backref='organizer', lazy='dynamic')  # New relationship to Event

    def __repr__(self):
        return f"User(Name: {self.name}, Email: {self.emailid})"

class Event(db.Model):
    __tablename__ = 'event'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Ensure this matches
    # event_name = db.Column(db.String(100), nullable=False)  # Ensure this matches
    description = db.Column(db.String(500))
    event_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Ensure this line exists

    # Define the relationship with the Order model
    orders = db.relationship('Order', back_populates='event', cascade='all, delete-orphan', lazy='dynamic')

    # Other relationships
    bookings = db.relationship('Booking', backref='event', lazy=True)
    comments = db.relationship('Comment', back_populates='event', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f"Event(Name: {self.event_name}, Date: {self.event_date})"

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(50), default='confirmed')

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='comments')
    event = db.relationship('Event', back_populates='comments')

    def __repr__(self):
        return f"Comment: {self.text} by User ID: {self.user_id}"

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)  # Use string reference
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(50), default='pending')

    # Relationships
    user = db.relationship('User', back_populates='orders')  # Ensure this relationship is correct
    event = db.relationship('Event', back_populates='orders')  # Ensure this is correctly defined
