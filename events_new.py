from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Step 1: Define your database connection URL
DATABASE_URL = 'sqlite:///events.db'  # Update this URL for your database (e.g., PostgreSQL, MySQL)

# Step 2: Create the database engine
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Step 3: Define the Events Table
class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String, nullable=False)                # Name of the event
    event_date = Column(DateTime, nullable=False)              # Date and time of the event
    location = Column(String)                                  # Location of the event
    description = Column(String)                               # Optional description
    organizer_name = Column(String, nullable=True)             # Organizer of the event

# Step 4: Create all tables in the database
Base.metadata.create_all(engine)

# Step 5: Create a session for interacting with the database
Session = sessionmaker(bind=engine)
session = Session()

# Step 6: Add sample event data (Brisbane Music Festival)
new_event = Event(
    event_name='Brisbane Music Festival',
    event_date='2024-12-01 18:00:00',  # Example datetime for the event
    location='Brisbane, QLD',
    description='A festival celebrating live music performances in Brisbane.',
    organizer_name='Brisbane Music Committee'
)
session.add(new_event)
session.commit()

# Step 7: Query and print all events to verify everything works
for event in session.query(Event).all():
    print(f'Event: {event.event_name}, Date: {event.event_date}, Location: {event.location}, Organizer: {event.organizer_name}')
