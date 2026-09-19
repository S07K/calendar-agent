from app.services.calendar_service import CalendarService
from app.tools.calendar_tools import create_calendar_event, get_calendar_event, list_calendar_events

class AgentService():
    def __init__(self, calendar_service: CalendarService) -> None:
        self.tools = {
            "create_calendar_event": create_calendar_event,
            "list_calendar_events": list_calendar_events,
            "get_calendar_event": get_calendar_event,
        }
        self.calendar_service = calendar_service

    def run(self, tool: str, arguments: dict | None = None):
        fn = self.tools.get(tool)
        arguments = arguments or {}
        if not fn:
            return fn
        return fn(self.calendar_service, **arguments)