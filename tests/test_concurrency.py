import pytest
import asyncio
from httpx import AsyncClient
from app.main import app
from app.db import init_db

@pytest.mark.asyncio
async def test_concurrent_idempotent_event_creation():
    await init_db()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # create shipment
        r = await ac.post('/shipments/', json={'external_id':'TST-RACE','status':'created'})
        assert r.status_code == 200
        s = r.json()
        sid = s['id']

        # prepare two concurrent requests with same idempotency key
        async def post_event(payload):
            return await ac.post(f'/shipments/{sid}/events', json=payload)

        payload = {'event_type':'pickup','payload':{'x':1}, 'idempotency_key':'race-key'}
        # run two requests concurrently
        r1, r2 = await asyncio.gather(post_event(payload), post_event(payload))
        assert r1.status_code == 200
        assert r2.status_code == 200
        e1 = r1.json()
        e2 = r2.json()
        # both should refer to the same event id
        assert e1['id'] == e2['id']

        # list events and ensure only one created with that id
        r3 = await ac.get(f'/shipments/{sid}/events')
        arr = r3.json()
        assert len([ev for ev in arr if ev['id']==e1['id']]) == 1
