from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Step 1: Define your database connection URL
# For testing with SQLite. Change this to your target DB like PostgreSQL, MySQL, etc.
DATABASE_URL = 'sqlite:///booking.db'

# Step 2: Create the database engine
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Step 3: Define the `Users` Table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)

    # Relationship to link bookings
    bookings = relationship("Booking", back_populates="user")

# Step 4: Define the `Events` Table
class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String, nullable=False)
    event_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    location = Column(String, nullable=True)
    description = Column(String, nullable=True)
    organizer_name = Column(String, nullable=True)

    # Relationship to link bookings
    bookings = relationship("Booking", back_populates="event")

# Step 5: Define the `Bookings` Table (junction table between Users and Events)
class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    booking_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='confirmed')  # Booking status: confirmed, canceled, etc.

    # Relationships to reference `User` and `Event` objects
    user = relationship("User", back_populates="bookings")
    event = relationship("Event", back_populates="bookings")

# Step 6: Create All Tables in the Database
Base.metadata.create_all(engine)

# Step 7: Create a session for interacting with the database
Session = sessionmaker(bind=engine)
session = Session()

# Step 8: Insert Sample Data into the Users and Events Tables
# Sample Users
user1 = User(username='alice', email='alice@example.com')
user2 = User(username='bob', email='bob@example.com')
session.add(user1)
session.add(user2)

# Sample Events
event1 = Event(event_name='Python Workshop', event_date='2024-11-01 10:00:00', location='Online', description='Learn Python basics and advanced topics.', organizer_name='Tech Academy')
event2 = Event(event_name='Data Science Summit', event_date='2024-12-15 09:00:00', location='New York', description='Explore the latest in Data Science and AI.', organizer_name='Data Science Org')
session.add(event1)
session.add(event2)

# Commit Users and Events to the Database
session.commit()

# Step 9: Create a Sample Booking
booking1 = Booking(user_id=user1.id, event_id=event1.id, status='confirmed')
session.add(booking1)
session.commit()

# Step 10: Query and Output All Bookings
for booking in session.query(Booking).all():
    user = session.query(User).filter_by(id=booking.user_id).first()
    event = session.query(Event).filter_by(id=booking.event_id).first()
    print(f'User: {user.username}, Event: {event.event_name}, Status: {booking.status}')
