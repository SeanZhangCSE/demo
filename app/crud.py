from typing import Optional
from uuid import UUID
from datetime import datetime
from sqlmodel import select
from app.models import Shipment, Event
from app.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

async def create_shipment(session: AsyncSession, external_id: Optional[str]=None, status: str="created", metadata: Optional[dict]=None) -> Shipment:
    shipment = Shipment(external_id=external_id, status=status, metadata=metadata)
    session.add(shipment)
    await session.commit()
    await session.refresh(shipment)
    return shipment

async def get_shipment(session: AsyncSession, shipment_id: UUID) -> Optional[Shipment]:
    return await session.get(Shipment, shipment_id)

async def create_event(session: AsyncSession, shipment_id: UUID, event_type: str, occurred_at: Optional[datetime]=None, payload: Optional[dict]=None, idempotency_key: Optional[str]=None) -> Event:
    # optional idempotency: if idempotency_key provided, avoid duplicate for same shipment
    if idempotency_key:
        q = select(Event).where(Event.shipment_id==shipment_id, Event.idempotency_key==idempotency_key)
        res = await session.exec(q)
        existing = res.first()
        if existing:
            return existing

    event = Event(shipment_id=shipment_id, event_type=event_type, occurred_at=occurred_at or datetime.utcnow(), payload=payload, idempotency_key=idempotency_key)
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event

async def list_events_for_shipment(session: AsyncSession, shipment_id: UUID, limit: int=100, offset: int=0):
    q = select(Event).where(Event.shipment_id==shipment_id).order_by(Event.occurred_at).limit(limit).offset(offset)
    res = await session.exec(q)
    return res.all()

async def query_events(session: AsyncSession, event_type: Optional[str]=None, limit: int=100, offset: int=0):
    q = select(Event)
    if event_type:
        q = q.where(Event.event_type==event_type)
    q = q.order_by(Event.occurred_at).limit(limit).offset(offset)
    res = await session.exec(q)
    return res.all()
