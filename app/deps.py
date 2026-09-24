from app.config import Settings
from app.services.agent_service import AgentService
from app.services.calendar_service import CalendarService
from app.services.notification_service import NotificationService
from app.workers.notification_worker import NotificationWorker

notification_service = NotificationService()
notification_worker = NotificationWorker(notification_service, interval_seconds=5)
calendar_service = CalendarService(notification_service)
settings = Settings()
agent_service = AgentService(calendar_service, settings)


def get_calendar_service() -> CalendarService:
    return calendar_service

def get_notification_service() -> NotificationService:
    return notification_service

def get_agent_service() -> AgentService:
    return agent_service

def get_notification_worker() -> NotificationWorker:
    return notification_worker