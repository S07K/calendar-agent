from app.services.agent_service import AgentService
from app.services.calendar_service import CalendarService
from app.services.notification_service import NotificationService

notification_service = NotificationService()
calendar_service = CalendarService(notification_service)
agent_service = AgentService(calendar_service)

def get_calendar_service() -> CalendarService:
    return calendar_service

def get_notification_service() -> NotificationService:
    return notification_service

def get_agent_service() -> AgentService:
    return agent_service