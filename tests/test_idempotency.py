import pytest
import asyncio
from httpx import AsyncClient
from app.main import app
from app.db import init_db

@pytest.mark.asyncio
async def test_idempotent_event_creation():
    await init_db()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # create shipment
        r = await ac.post('/shipments/', json={'external_id':'TST-IDEMP','status':'created'})
        assert r.status_code == 200
        s = r.json()
        sid = s['id']

        # post event with idempotency key
        r1 = await ac.post(f'/shipments/{sid}/events', json={'event_type':'pickup','payload':{'x':1}, 'idempotency_key':'key-123'})
        assert r1.status_code == 200
        e1 = r1.json()

        # post again with same idempotency key
        r2 = await ac.post(f'/shipments/{sid}/events', json={'event_type':'pickup','payload':{'x':2}, 'idempotency_key':'key-123'})
        assert r2.status_code == 200
        e2 = r2.json()

        # should return the same event id (no duplicate created)
        assert e1['id'] == e2['id']

        # list events and ensure only one
        r3 = await ac.get(f'/shipments/{sid}/events')
        arr = r3.json()
        # at least one event should exist; idempotent duplicate shouldn't add another
        assert sum(1 for ev in arr if ev['id'] == e1['id']) == 1
