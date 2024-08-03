from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Base class for declarative class definitions
Base = declarative_base()

# URL model representing the URL table in the database
class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each URL
    short_url = Column(String, unique=True, index=True)  # Shortened URL
    original_url = Column(String, nullable=False)  # Original URL
    expiry_time = Column(DateTime, nullable=True)  # Expiry time for the URL
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Timestamp of creation
