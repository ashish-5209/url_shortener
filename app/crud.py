from sqlalchemy.orm import Session
from .models import URL
from .schemas import URLCreate
from datetime import datetime
import string

# Base62 characters
BASE62 = string.ascii_letters + string.digits

# Function to encode an integer into base62
def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]
    arr = []
    base = len(BASE62)
    while num:
        num, rem = divmod(num, base)
        arr.append(BASE62[rem])
    arr.reverse()
    return ''.join(arr)

# Function to create a new URL entry in the database
def create_url(db: Session, url: URLCreate) -> URL:
    # Check if there's an existing valid short URL for the given original URL
    existing_url = db.query(URL).filter(URL.original_url == str(url.original_url)).first()
    
    if existing_url:
        # If the existing URL is not expired, return it
        if existing_url.expiry_time and existing_url.expiry_time >= datetime.now():
            return existing_url
        
        # If the existing URL is expired, delete it
        db.delete(existing_url)
        db.commit()
    
    # Get the current highest ID in the database and increment it
    highest_id = db.query(URL).order_by(URL.id.desc()).first()
    new_id = 1 if highest_id is None else highest_id.id + 1
    
    # Encode the new ID to a base62 short URL
    short_url = encode_base62(new_id)
    
    # Create and store the new URL object
    db_url = URL(id=new_id, short_url=short_url, original_url=str(url.original_url), expiry_time=url.expiry_time)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


# Function to retrieve a URL entry from the database using the short URL
def get_url(db: Session, short_url: str):
    db_url = db.query(URL).filter(URL.short_url == short_url).first()
    if db_url is None:
        # Handle the case where no URL was found
        return None
    return db_url


# Function to delete expired URLs from the database
def delete_expired_urls(db: Session):
    now = datetime.utcnow()
    expired_urls = db.query(URL).filter(URL.expiry_time < now).all()  # Retrieve expired URLs
    for url in expired_urls:
        db.delete(url)  # Delete each expired URL
    db.commit()
