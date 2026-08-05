import pytest
from httpx import AsyncClient
from app.main import app
from app.db import init_db

@pytest.mark.asyncio
async def test_patch_shipment():
    await init_db()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post('/shipments/', json={'external_id':'TST-UPD','status':'created'})
        assert r.status_code == 200
        s = r.json()
        sid = s['id']

        # patch status
        r2 = await ac.patch(f'/shipments/{sid}', json={'status':'in_transit'})
        assert r2.status_code == 200
        updated = r2.json()
        assert updated['status'] == 'in_transit'
