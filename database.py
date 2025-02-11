import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the database engine (replace with your actual database URI)
SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_URL")

# Create the engine that will interact with the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a base class for your models to inherit from
Base = declarative_base()

# Create the session maker for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for getting the database session in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
