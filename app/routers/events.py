from fastapi import APIRouter, Depends
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import get_session
import app.crud as crud
from app.schemas import EventRead

router = APIRouter()

@router.get("/", response_model=list[EventRead])
async def list_events(event_type: Optional[str] = None, limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)):
    """Global query endpoint for events.

    Query params:
    - event_type: optional filter by event_type
    - limit/offset: pagination
    """
    events = await crud.query_events(session, event_type=event_type, limit=limit, offset=offset)
    return events
