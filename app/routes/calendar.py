from fastapi import APIRouter, Depends, HTTPException
from app.schemas import EventCreate, EventResponse
from app.deps import get_calendar_service
from app.services.calendar_service import CalendarService

router = APIRouter(
    prefix="/events",
    tags=["events"]
)

@router.get("/", response_model=list[EventResponse])
def get_events(service: CalendarService = Depends(get_calendar_service)):
    events = service.get_events()
    return events

@router.post("/", response_model=EventResponse)
def create_event(event: EventCreate, service: CalendarService = Depends(get_calendar_service)):
    event_created = service.create_event(event)
    if(event_created is None):
        raise HTTPException(status_code=409, detail="Slot not available")
    return event_created

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: str, service: CalendarService = Depends(get_calendar_service)):
    event = service.get_event(event_id)
    if(event is None):
        raise HTTPException(status_code=404, detail="Event Not Found")
    return event