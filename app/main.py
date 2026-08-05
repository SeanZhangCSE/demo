from fastapi import FastAPI
from app.db import init_db
from app.routers import shipments, events

app = FastAPI(title="Shipment Events Service")

app.include_router(shipments.router, prefix="/shipments", tags=["shipments"])
app.include_router(events.router, prefix="/events", tags=["events"])

@app.on_event("startup")
async def on_startup():
    await init_db()
