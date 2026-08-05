from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from sqlalchemy.sql import func

class Shipment(SQLModel, table=True):
    __tablename__ = "shipments"

    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    external_id: Optional[str] = Field(default=None, index=True)
    status: str = Field(default="created", index=True)
    metadata: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    events: list["Event"] = Relationship(back_populates="shipment")

class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    shipment_id: UUID = Field(foreign_key="shipments.id", index=True, nullable=False)
    event_type: str = Field(index=True)
    occurred_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    payload: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    idempotency_key: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    shipment: Optional[Shipment] = Relationship(back_populates="events")
