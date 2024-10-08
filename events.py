import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Step 1: Define the database engine (adjust the URL to match your database)
DATABASE_URL = 'sqlite:///events.db'  # You can change this to any supported database, e.g., PostgreSQL, MySQL, or SQL Server

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Step 2: Define the Events Table
class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary Key
    event_name = Column(String, nullable=False)                # Name of the event
    event_date = Column(DateTime, nullable=False)              # Date and time of the event
    location = Column(String)                                  # Location of the event
    description = Column(String)                               # Optional description
    organizer_name = Column(String, nullable=True)             # Organizer of the event

# Step 3: Create All Tables in the Database
Base.metadata.create_all(engine)

# Step 4: Create a Session for Adding and Querying Data
Session = sessionmaker(bind=engine)
session = Session()

# Step 5: Insert a Sample Event into the Events Table
new_event = Event(
    event_name='Tech Conference 2024',
    event_date='2024-11-15 09:00:00',  # Use a datetime object in actual scenarios
    location='New York, NY',
    description='A conference discussing emerging tech trends.',
    organizer_name='Tech Events Inc.'
)
session.add(new_event)
session.commit()

# Step 6: Query and Output All Events
for event in session.query(Event).all():
    print(f'Event: {event.event_name}, Date: {event.event_date}, Location: {event.location}, Organizer: {event.organizer_name}')
