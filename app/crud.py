"""CRUD helpers for Shipments and Events.

This module contains database operations used by the HTTP handlers. Functions
are written for use with an async SQLModel/SQLAlchemy AsyncSession. Each
function documents its purpose, parameters, return value, and any important
side-effects or assumptions (e.g. idempotency behavior).
"""
from typing import Optional
from uuid import UUID
from datetime import datetime
from sqlmodel import select
from app.models import Shipment, Event
from sqlmodel.ext.asyncio.session import AsyncSession


async def create_shipment(session: AsyncSession, external_id: Optional[str] = None, status: str = "created", metadata: Optional[dict] = None) -> Shipment:
    """Create and persist a Shipment record.

    Args:
        session: Async SQLModel session (in a FastAPI dependency this comes from get_session).
        external_id: Optional external identifier provided by clients.
        status: Initial status string (defaults to "created").
        metadata: Optional JSON-serializable metadata stored in a JSONB column.

    Returns:
        The persisted Shipment instance with generated id and timestamps filled.

    Side-effects:
        Commits the session.
    """
    shipment = Shipment(external_id=external_id, status=status, metadata=metadata)
    session.add(shipment)
    await session.commit()
    await session.refresh(shipment)
    return shipment


async def get_shipment(session: AsyncSession, shipment_id: UUID) -> Optional[Shipment]:
    """Fetch a Shipment by its primary key.

    Returns None if not found.
    """
    return await session.get(Shipment, shipment_id)


async def create_event(session: AsyncSession, shipment_id: UUID, event_type: str, occurred_at: Optional[datetime] = None, payload: Optional[dict] = None, idempotency_key: Optional[str] = None) -> Event:
    """Create and persist an Event attached to a Shipment.

    Idempotency behavior:
        If `idempotency_key` is provided, the function first queries for an
        existing Event with the same shipment_id and idempotency_key and returns
        it if found instead of inserting a duplicate. This pattern provides a
        simple at-least-once to exactly-once upgrade for callers that can supply
        a stable idempotency key.

    Args:
        session: Async SQLModel session.
        shipment_id: UUID of an existing Shipment (caller should ensure it exists).
        event_type: A string describing the event (e.g. 'pickup', 'delivery').
        occurred_at: Timestamp when the event occurred. If omitted, UTC now is used.
        payload: Optional JSON payload with event details.
        idempotency_key: Optional string used to deduplicate repeated requests.

    Returns:
        The persisted Event instance (existing one if idempotent duplicate).

    Side-effects:
        Commits the session on insert.
    """
    # optional idempotency: if idempotency_key provided, avoid duplicate for same shipment
    if idempotency_key:
        q = select(Event).where(Event.shipment_id == shipment_id, Event.idempotency_key == idempotency_key)
        res = await session.exec(q)
        existing = res.first()
        if existing:
            return existing

    event = Event(shipment_id=shipment_id, event_type=event_type, occurred_at=occurred_at or datetime.utcnow(), payload=payload, idempotency_key=idempotency_key)
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


async def list_events_for_shipment(session: AsyncSession, shipment_id: UUID, limit: int = 100, offset: int = 0):
    """Return a page of events for a given shipment ordered by occurred_at.

    Simple limit/offset pagination is used. The default limit is 100.
    """
    q = select(Event).where(Event.shipment_id == shipment_id).order_by(Event.occurred_at).limit(limit).offset(offset)
    res = await session.exec(q)
    return res.all()


async def query_events(session: AsyncSession, event_type: Optional[str] = None, limit: int = 100, offset: int = 0):
    """Query events globally with optional filtering by event_type.

    Args:
        event_type: Optional type string to filter events.
        limit, offset: Pagination parameters.

    Returns:
        List of Event instances matching the query.
    """
    q = select(Event)
    if event_type:
        q = q.where(Event.event_type == event_type)
    q = q.order_by(Event.occurred_at).limit(limit).offset(offset)
    res = await session.exec(q)
    return res.all()
