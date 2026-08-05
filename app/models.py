"""Data models for shipments and events.

Shipment
    - id: UUID primary key
    - external_id: optional external identifier (indexable)
    - status: shipping status (indexed)
    - metadata: arbitrary JSON metadata stored in JSONB
    - created_at / updated_at: timestamps using UTC

Event
    - id: UUID primary key
    - shipment_id: FK to shipments.id
    - event_type: category of event (indexed)
    - occurred_at: timestamp when the event actually occurred
    - payload: arbitrary JSON data for the event
    - idempotency_key: optional key to deduplicate repeated event submissions
"""
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship, Column, JSON


class Shipment(SQLModel, table=True):
    __tablename__ = "shipments"

    # Primary key UUID generated server-side
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)

    # An optional external identifier to map to other systems. Indexed for lookup.
    external_id: Optional[str] = Field(default=None, index=True)

    # Current shipment status (e.g., created, in_transit, delivered)
    status: str = Field(default="created", index=True)

    # Arbitrary JSON metadata; stored in a JSONB column via sa_column
    metadata: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    # Timestamps are naive UTC datetimes by default (datetime.utcnow())
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship: list of associated events
    events: list["Event"] = Relationship(back_populates="shipment")


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    shipment_id: UUID = Field(foreign_key="shipments.id", index=True, nullable=False)

    # A short string representing the event category
    event_type: str = Field(index=True)

    # When the event occurred in real world time
    occurred_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # JSON payload with event-specific data
    payload: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    # Optional key allowing clients to retry safely without creating duplicates
    idempotency_key: Optional[str] = Field(default=None, index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Back-reference to the shipment
    shipment: Optional[Shipment] = Relationship(back_populates="events")
