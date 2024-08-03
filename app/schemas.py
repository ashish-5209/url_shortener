from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

# Schema for URL creation request
class URLCreate(BaseModel):
    original_url: HttpUrl  # The original URL to be shortened
    expiry_time: Optional[datetime] = None  # Optional expiry time

# Schema for URL response
class URLResponse(BaseModel):
    short_url: str  # The generated short URL
    original_url: HttpUrl  # The original URL
    expiry_time: Optional[datetime] = None  # Optional expiry time
