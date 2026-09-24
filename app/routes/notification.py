from datetime import datetime
from fastapi import APIRouter, Depends
from app.deps import get_notification_service, get_notification_worker
from app.schemas import Notification
from app.services.notification_service import NotificationService
from app.workers.notification_worker import NotificationWorker

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)

@router.get("/", response_model=list[Notification])
def get_notifications(service: NotificationService = Depends(get_notification_service)):
    notifications = service.get_notifications()
    return notifications

@router.post("/dispatch", response_model=list[Notification])
def dispatch_due(now: datetime | None = None, service: NotificationService = Depends(get_notification_service), worker: NotificationWorker = Depends(get_notification_worker)):
    now = now or datetime.now()
    notifications_fired = service.dispatch_due(now)
    return notifications_fired