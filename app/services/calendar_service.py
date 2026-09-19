from datetime import timedelta
from uuid import uuid4
from app.schemas import EventCreate
from app.services.notification_service import NotificationService

class CalendarService():
    def __init__(self, notification_service: NotificationService):
        self.events = {}
        self.notification_service = notification_service

    def _end_time(self, start, duration_minutes):
        return start + timedelta(minutes=duration_minutes)
    def create_event(self, event: EventCreate):
        event_start_time = event.start_time
        event_end_time = self._end_time(start=event_start_time, duration_minutes=event.duration_minutes)
        for existing_event in self.events.values():
            existing_start_time = existing_event['start_time']
            existing_end_time = self._end_time(start=existing_event['start_time'], duration_minutes=existing_event['duration_minutes'])
            if existing_start_time < event_end_time and existing_end_time > event_start_time:
                return None

        id = str(uuid4())
        new_event = {
            "id": id,
            "title": event.title,
            "start_time": event.start_time,
            "duration_minutes": event.duration_minutes
        }
        self.events[id] = new_event
        self.notification_service.schedule_notification(id, event.start_time, "reminder_5min")
        self.notification_service.schedule_notification(id, event.start_time, "start")
        return new_event

    def get_event(self, id: str):
        return self.events.get(id)

    def get_events(self):
        return list(self.events.values())