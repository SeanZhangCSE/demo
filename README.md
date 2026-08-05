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
