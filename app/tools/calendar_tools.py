from datetime import datetime
from app.schemas import EventCreate
from app.services.calendar_service import CalendarService

def create_calendar_event(calendar_service: CalendarService, title: str, start_time: datetime, duration_minutes: int):
    event = EventCreate(
        title=title,
        start_time=start_time,
        duration_minutes=duration_minutes
    )
    created_event = calendar_service.create_event(event)
    return created_event

def list_calendar_events(calendar_service: CalendarService):
    return calendar_service.get_events()

def get_calendar_event(calendar_service: CalendarService, event_id: str):
    return calendar_service.get_event(id=event_id)