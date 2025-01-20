from database import engine, Base
import models
# Create all tables in the database
print("Creating database tables...")
Base.metadata.drop_all(bind=engine)  # Drop all existing tables
Base.metadata.create_all(bind=engine)  # Create tables from updated models
print("Tables created successfully!")
