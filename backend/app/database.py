import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv() # Load the .env file

DATABASE_URL = os.environ["DATABASE_URL"]

# The "engine" is the main connection point
engine = create_engine(DATABASE_URL)

# The "SessionLocal" is a *factory* that will create
# new "conversation" objects for us.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A simple function to get a new database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()