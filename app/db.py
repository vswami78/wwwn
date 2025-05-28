from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import DB_URL

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    # This function will be called from app.py to create tables
    # Import all modules here that define models so that
    # they are registered with Base.metadata
    from app import models # Add this import here
    Base.metadata.create_all(bind=engine)
