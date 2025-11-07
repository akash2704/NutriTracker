import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv() # Load the .env file

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Use SQLite for testing if no DATABASE_URL is provided
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./nutritracker.db"

# Configure engine based on database type
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# The "SessionLocal" is a *factory* that will create
# new "conversation" objects for us.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base for models
Base = declarative_base()

# A simple function to get a new database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()