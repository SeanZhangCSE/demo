# simple seed script to insert example shipments and events
import asyncio
import os
from datetime import datetime, timedelta
from uuid import uuid4
from sqlmodel import SQLModel
from app.db import engine
from app.models import Shipment, Event

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with engine.begin() as conn:
        # insert sample shipment
        s1 = Shipment(id=uuid4(), external_id='SAMPLE-1', status='in_transit', metadata={'carrier':'ACME'})
        await conn.run_sync(lambda sync_conn: sync_conn.execute(Shipment.__table__.insert().values(
            id=s1.id, external_id=s1.external_id, status=s1.status, metadata=s1.metadata, created_at=s1.created_at, updated_at=s1.updated_at
        )))

        e1 = Event(id=uuid4(), shipment_id=s1.id, event_type='pickup', occurred_at=datetime.utcnow(), payload={'location':'warehouse'}, idempotency_key='seed-1')
        await conn.run_sync(lambda sync_conn: sync_conn.execute(Event.__table__.insert().values(
            id=e1.id, shipment_id=e1.shipment_id, event_type=e1.event_type, occurred_at=e1.occurred_at, payload=e1.payload, idempotency_key=e1.idempotency_key, created_at=e1.created_at
        )))

if __name__ == '__main__':
    asyncio.run(seed())
