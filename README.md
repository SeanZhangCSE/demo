# Quick README

# Shipment Events Service (Take-home)

This is an async FastAPI service implementing a simple Shipment and Event model using SQLModel + PostgreSQL.

Quick start (development):

1. Start services:

   docker-compose up --build

2. Apply migrations (in another shell):

   docker-compose exec app alembic upgrade head

   (If Alembic is not configured to connect automatically, set DATABASE_URL env var.)

3. Optionally seed data:

   docker-compose exec app python scripts/seed.py

4. API is available at http://localhost:8000

Endpoints:
- POST /shipments/ — create shipment
- GET /shipments/{id} — get shipment
- POST /shipments/{id}/events — add event
- GET /shipments/{id}/events — list events for shipment
- GET /events — global event query

Notes:
- Implementation uses async SQLModel and asyncpg.
- Alembic migration included at alembic/versions/0001_create_tables.py
- For quick local dev, the app will create tables automatically on startup if missing.


## Implementation details & assumptions

This project was implemented to satisfy the TakeHome "Shipment Events Service" requirements (PDF in repository). Key implementation decisions and assumptions made during development:

- Idempotency: Events support an optional `idempotency_key` field. When present, the service will return an existing event for the same shipment and idempotency_key instead of creating a duplicate.
- Pagination: Endpoints use simple limit/offset pagination with a default limit of 100. If cursor-based pagination is required, it can be added later.
- Time handling: Timestamps are stored as naive UTC datetimes (created using datetime.utcnow()). Responses expose ISO-style datetimes via Pydantic models in FastAPI. If timezone-aware datetimes are required, we can switch to timezone-aware columns and ISO formatting.
- Authentication: No authentication is implemented by default. If required, API-key or JWT middleware can be added.
- Alembic + asyncpg: Alembic does not migrate using the asyncpg driver directly. The alembic/env.py script adjusts the URL for migration runs to use the sync driver. For local dev it's simplest to run migrations inside the `app` container where DATABASE_URL is already set.


## Running with minimal local setup (no Python required)

1) Install Docker
2) git clone <repo> && cd repo
3) docker-compose up --build
4) docker-compose exec app alembic upgrade head
5) (Optional) docker-compose exec app python scripts/seed.py
6) Visit http://localhost:8000/docs


## Running tests inside container

docker-compose exec app pytest -q
