from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Step 1: Define your database connection URL
# SQLite for local testing; update this to use other databases like PostgreSQL, MySQL, etc.
DATABASE_URL = 'sqlite:///user_management.db'

# Step 2: Create the database engine
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Step 3: Define the `Roles` Table (optional)
class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String, nullable=False, unique=True)  # e.g., Admin, Guest, User
    description = Column(String, nullable=True)

    # Relationship to link with users
    users = relationship("User", back_populates="role")

# Step 4: Define the `Users` Table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)   # Username for login
    email = Column(String, nullable=False, unique=True)      # Email address of the user
    full_name = Column(String, nullable=True)                # User's full name
    created_at = Column(DateTime, default=datetime.utcnow)   # Timestamp for user creation
    role_id = Column(Integer, ForeignKey('roles.id'))        # Foreign Key to `Roles` table

    # Relationship to reference Role
    role = relationship("Role", back_populates="users")

# Step 5: Create All Tables in the Database
Base.metadata.create_all(engine)

# Step 6: Create a session for interacting with the database
Session = sessionmaker(bind=engine)
session = Session()

# Step 7: Insert Sample Data into the Roles Table (Optional)
# Adding sample roles
admin_role = Role(role_name='Admin', description='Administrator with full access')
user_role = Role(role_name='User', description='Regular user with limited access')
session.add(admin_role)
session.add(user_role)
session.commit()

# Step 8: Insert Sample Users into the Users Table
user1 = User(username='johndoe', email='john.doe@example.com', full_name='John Doe', role_id=admin_role.id)
user2 = User(username='janedoe', email='jane.doe@example.com', full_name='Jane Doe', role_id=user_role.id)
session.add(user1)
session.add(user2)
session.commit()

# Step 9: Query and Output All Users
for user in session.query(User).all():
    role = session.query(Role).filter_by(id=user.role_id).first()
    print(f'User: {user.username}, Email: {user.email}, Full Name: {user.full_name}, Role: {role.role_name}')
