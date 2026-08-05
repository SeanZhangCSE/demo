import pytest
from httpx import AsyncClient
from app.main import app
from app.db import init_db

@pytest.mark.asyncio
async def test_event_query_filtering():
    await init_db()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post('/shipments/', json={'external_id':'TST-Q','status':'created'})
        assert r.status_code == 200
        s = r.json()
        sid = s['id']

        # create events of different types
        await ac.post(f'/shipments/{sid}/events', json={'event_type':'pickup','payload':{'a':1}})
        await ac.post(f'/shipments/{sid}/events', json={'event_type':'delivery','payload':{'b':2}})
        await ac.post(f'/shipments/{sid}/events', json={'event_type':'pickup','payload':{'c':3}})

        # query global events by type
        r2 = await ac.get('/events', params={'event_type':'pickup'})
        assert r2.status_code == 200
        arr = r2.json()
        # should include at least two pickup events
        assert len([e for e in arr if e['event_type']=='pickup']) >= 2
