# URL Shortener API

A FastAPI-based URL shortener service that stores original URLs, generates short codes, tracks clicks, and supports optional expiration for shortened links.

## Features

- Create shortened URLs with random unique short codes
- Redirect short codes to original URLs
- Track click counts on every redirect
- Fetch analytics for any short code
- Support expiration with `expiry_days` or `expires_at`
- Validate request payloads and return structured error responses

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Python

## Project Structure

```text
app/
├── api/
│   ├── router.py
│   └── routes/
├── core/
├── crud/
├── db/
├── models/
├── schemas/
├── services/
└── utils/
```

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Copy the example environment file and update database settings if needed:

```bash
cp .env.example .env
```

3. Start the API:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Environment Variables

The application supports the following configuration values:

- `PROJECT_NAME`
- `VERSION`
- `DESCRIPTION`
- `API_PREFIX`
- `DEBUG`
- `HOST`
- `PORT`
- `DATABASE_URL`
- `DATABASE_ECHO`

## API Endpoints

### `POST /shorten`

Create a new short URL.

Request body:

```json
{
  "original_url": "https://example.com/some/long/path",
  "expiry_days": 7
}
```

You can also provide an explicit expiration timestamp instead of `expiry_days`:

```json
{
  "original_url": "https://example.com",
  "expires_at": "2026-04-30T12:00:00Z"
}
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url":"https://example.com/docs","expiry_days":7}'
```

Sample response:

```json
{
  "id": 1,
  "original_url": "https://example.com/docs",
  "short_code": "aB12Cd",
  "short_url": "http://127.0.0.1:8000/aB12Cd",
  "clicks": 0,
  "created_at": "2026-03-28T12:00:00Z",
  "expires_at": "2026-04-04T12:00:00Z"
}
```

### `GET /stats/{short_code}`

Fetch analytics for a shortened URL.

Example:

```bash
curl http://127.0.0.1:8000/stats/aB12Cd
```

Sample response:

```json
{
  "short_code": "aB12Cd",
  "original_url": "https://example.com/docs",
  "clicks": 3,
  "created_at": "2026-03-28T12:00:00Z",
  "expires_at": "2026-04-04T12:00:00Z"
}
```

### `GET /{short_code}`

Redirect to the original URL and increment the click count.

Example:

```bash
curl -i http://127.0.0.1:8000/aB12Cd
```

### `GET /health`

Basic health check endpoint.

Example:

```bash
curl http://127.0.0.1:8000/health
```

Sample response:

```json
{
  "success": true,
  "message": "Service is healthy.",
  "data": {
    "status": "ok"
  }
}
```

## Error Response Format

Invalid requests and runtime API errors return a consistent error shape:

```json
{
  "success": false,
  "error": {
    "code": "validation_error",
    "message": "Invalid request payload.",
    "details": [
      {
        "field": "original_url",
        "message": "invalid or missing URL scheme"
      }
    ]
  }
}
```

## Notes

- URL tables are created automatically on application startup.
- The default database connection string targets PostgreSQL on `localhost`.
- Interactive API docs are available at `/docs`.
