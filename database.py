from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize the database engine (replace with your actual database URI)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:vipul8318@localhost:5432/medigos"

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
