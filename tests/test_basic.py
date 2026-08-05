import pytest
import asyncio
from httpx import AsyncClient
from app.main import app
from app.db import init_db

@pytest.mark.asyncio
async def test_create_shipment_and_event():
    await init_db()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # create shipment
        r = await ac.post('/shipments/', json={'external_id':'TST-1','status':'created'})
        assert r.status_code == 200
        s = r.json()
        sid = s['id']

        # post event
        r2 = await ac.post(f'/shipments/{sid}/events', json={'event_type':'pickup','payload':{'x':1}})
        assert r2.status_code == 200
        e = r2.json()
        assert e['shipment_id'] == sid

        # list events
        r3 = await ac.get(f'/shipments/{sid}/events')
        assert r3.status_code == 200
        arr = r3.json()
        assert len(arr) >= 1
