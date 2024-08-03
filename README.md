# URL Shortener Service

A simple URL shortener service implemented with FastAPI and SQLAlchemy. This service allows users to shorten URLs, handle redirections, and includes an expiry mechanism for short URLs and tracks performance metrics.

## Features

- Shorten URLs and generate unique short URLs
- Redirect to original URLs using short URLs
- Set expiry time for short URLs
- Track performance metrics such as the number of URLs shortened and redirected
- Configurable for different environments (development, pre-production, production)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/ashish-5209/url_shortener.git
    cd url_shortener
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file and set your environment variables:**
    ```env
    ENVIRONMENT=development
    HOST=0.0.0.0
    PORT=8000

    DATABASE_URL_DEV=postgresql://dev_user:dev_password@localhost/dev_dbname
    DATABASE_URL_PREPROD=postgresql://preprod_user:preprod_password@localhost/preprod_dbname
    DATABASE_URL_PROD=postgresql://prod_user:prod_password@localhost/prod_dbname

    SECRET_KEY=secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5. **Run database migrations:**
    ```bash
    alembic upgrade head
    ```

6. **Start the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

7. **Access the API documentation:**
    - Swagger UI: `http://127.0.0.1:8000/docs`
    - ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

### Create Short URL
- **Endpoint:** `/shorten`
- **Method:** `POST`
- **Request Body:** JSON containing the original URL and an optional expiry time.
- **Response:** JSON containing the unique short URL and its expiry time.

### Redirect to Original URL
- **Endpoint:** `/{short_url}`
- **Method:** `GET`
- **Response:** Redirect to the original URL if the short URL is valid and has not expired.

## Performance Metrics

The service tracks the following performance metrics:
- Number of URLs shortened.
- Number of redirects performed.
- Average response time for shortening a URL.
- Average response time for redirection.
