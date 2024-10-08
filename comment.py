from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Step 1: Define your database connection URL
DATABASE_URL = 'sqlite:///comments.db'  # Update to match your database (e.g., PostgreSQL, MySQL)

# Step 2: Create the database engine
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Step 3: Define the `Users` Table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    full_name = Column(String, nullable=True)

    # Relationship to link comments
    comments = relationship("Comment", back_populates="user")

# Step 4: Define the `Comments` Table
class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign Key to `Users` table
    content = Column(Text, nullable=False)                            # The actual comment content
    created_at = Column(DateTime, default=datetime.utcnow)            # Timestamp for when the comment was made
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for when the comment was last updated

    # Relationship to reference `User`
    user = relationship("User", back_populates="comments")

# Step 5: Create All Tables in the Database
Base.metadata.create_all(engine)

# Step 6: Create a session for interacting with the database
Session = sessionmaker(bind=engine)
session = Session()

# Step 7: Insert Sample Users into the Users Table
user1 = User(username='john_doe', email='john.doe@example.com', full_name='John Doe')
user2 = User(username='jane_doe', email='jane.doe@example.com', full_name='Jane Doe')
session.add(user1)
session.add(user2)
session.commit()

# Step 8: Insert Sample Comments into the Comments Table
comment1 = Comment(user_id=user1.id, content='This is a great article about SQLAlchemy!')
comment2 = Comment(user_id=user2.id, content='Thanks for sharing this information.')
session.add(comment1)
session.add(comment2)
session.commit()

# Step 9: Query and Output All Comments with User Information
for comment in session.query(Comment).all():
    user = session.query(User).filter_by(id=comment.user_id).first()
    print(f'User: {user.username}, Comment: {comment.content}, Created At: {comment.created_at}')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)

