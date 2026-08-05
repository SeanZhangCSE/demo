from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from app import schemas as s
from app.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
import app.crud as crud

router = APIRouter()

@router.post("/", response_model=s.ShipmentRead)
async def create_shipment(payload: s.ShipmentCreate, session: AsyncSession = Depends(get_session)):
    """Create a new shipment.

    Request body: ShipmentCreate
    Response: ShipmentRead (including generated id)
    """
    shipment = await crud.create_shipment(session, external_id=payload.external_id, status=payload.status, metadata=payload.metadata)
    return shipment


@router.get("/{shipment_id}", response_model=s.ShipmentRead)
async def get_shipment(shipment_id: UUID, session: AsyncSession = Depends(get_session)):
    """Return a shipment by id or 404 if not found."""
    shipment = await crud.get_shipment(session, shipment_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


@router.post("/{shipment_id}/events", response_model=s.EventRead)
async def create_event_for_shipment(shipment_id: UUID, payload: s.EventCreate, session: AsyncSession = Depends(get_session)):
    """Attach an event to a shipment.

    Supports optional idempotency via `idempotency_key` in the request body.
    If the key is supplied and an Event with the same shipment_id+idempotency_key
    exists, the existing Event is returned (no duplicate insert).
    """
    shipment = await crud.get_shipment(session, shipment_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    event = await crud.create_event(session, shipment_id=shipment_id, event_type=payload.event_type, occurred_at=payload.occurred_at, payload=payload.payload, idempotency_key=payload.idempotency_key)
    return event


@router.get("/{shipment_id}/events", response_model=list[s.EventRead])
async def list_events(shipment_id: UUID, limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)):
    """List events for a shipment (limit/offset pagination)."""
    shipment = await crud.get_shipment(session, shipment_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    events = await crud.list_events_for_shipment(session, shipment_id=shipment_id, limit=limit, offset=offset)
    return events
