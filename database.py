from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL Connection URL (Replace with your credentials)
DATABASE_URL = "postgresql://postgres:zaryab123@localhost:5432/daadrasDB"

# Create an engine to connect to PostgreSQL
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()