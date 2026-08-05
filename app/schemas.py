from sqlmodel import SQLModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class ShipmentCreate(BaseModel):
    external_id: Optional[str]
    status: Optional[str] = "created"
    metadata: Optional[dict]

class ShipmentRead(BaseModel):
    id: UUID
    external_id: Optional[str]
    status: str
    metadata: Optional[dict]
    created_at: datetime
    updated_at: datetime

class EventCreate(BaseModel):
    event_type: str
    occurred_at: Optional[datetime]
    payload: Optional[dict]
    idempotency_key: Optional[str]

class EventRead(BaseModel):
    id: UUID
    shipment_id: UUID
    event_type: str
    occurred_at: datetime
    payload: Optional[dict]
    idempotency_key: Optional[str]
    created_at: datetime
