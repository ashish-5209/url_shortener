from fastapi import FastAPI, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from .schemas import URLCreate, URLResponse
from .dependencies import get_db, engine
from .crud import create_url, get_url, delete_expired_urls
from .metrics import URLS_SHORTENED, URLS_REDIRECTED, REQUEST_TIME
from datetime import datetime
from .config import settings
import uvicorn
from .models import Base
import logging
from fastapi.responses import FileResponse
from pathlib import Path

logger = logging.getLogger("uvicorn")

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Initialize FastAPI application with metadata
app = FastAPI(
    title="URL Shortener Service",
    description="A simple URL shortener service with expiry mechanism and performance metrics",
    version="1.0.0",
)
@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Startup event to create the database tables and remove expired URLs
@app.on_event("startup")
async def startup_event():
    # Create database tables
    Base.metadata.create_all(bind=engine)
    # Remove expired URLs
    with next(get_db()) as db:
        delete_expired_urls(db)

# Endpoint to shorten a URL
@app.post("/shorten", response_model=URLResponse, tags=["URL Shortener"])
async def shorten_url(url: URLCreate, db: Session = Depends(get_db)):
    # Start the timer for the request
    with REQUEST_TIME.labels(method='POST', endpoint='/shorten').time():
        db_url = create_url(db, url)
        URLS_SHORTENED.inc()
        return db_url

# Endpoint to redirect to the original URL using the short URL
@app.get("/{short_url}", tags=["URL Shortener"])
async def redirect_url(short_url: str, db: Session = Depends(get_db)):
    db_url = get_url(db, short_url)
    if not db_url:
        logger.error(f"URL not found: {short_url}")
        raise HTTPException(status_code=404, detail="URL not found or expired")
    if db_url.expiry_time and db_url.expiry_time < datetime.utcnow():
        logger.error(f"URL expired: {short_url}")
        raise HTTPException(status_code=404, detail="URL not found or expired")
    URLS_REDIRECTED.inc()
    return db_url.original_url

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(Path(__file__).parent / "static" / "favicon.ico")

# Shutdown event to remove expired URLs
@app.on_event("shutdown")
def shutdown_event():
    # Use synchronous session management for shutdown
    with next(get_db()) as db:
        delete_expired_urls(db)

if __name__ == "__main__":
    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
