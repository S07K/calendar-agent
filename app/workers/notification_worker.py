import asyncio
import logging
from app.services.notification_service import NotificationService
from datetime import datetime

logger = logging.getLogger(__name__)

class NotificationWorker:
    def __init__(self, notification_service: NotificationService, interval_seconds: int = 10):
        self.notification_service = notification_service
        self.interval_seconds = interval_seconds

    async def start(self):
        """
        Continuously polls the notification service for due notifications.
        """
        logger.info("Notification worker has started...")
        while True:
            try:
                now = datetime.now()
                fired_notifications = self.notification_service.dispatch_due(now)

                for notification in fired_notifications:
                    await self._send_actual_notification(notification=notification)
            except Exception as e:
                logger.error(f"Error in notification worker loop: {e}")

            await asyncio.sleep(self.interval_seconds)



    async def _send_actual_notification(self, notification: dict):
        """
        Handles sending based on the kind
        """

        event_id = notification["event_id"]
        kind = notification["kind"]
        notify_at = notification["notify_at"]
        
        if kind == "reminder_5min":
            print(f"[ALERT] Reminder: Event {event_id} starts in 5 minutes! (at {notify_at})")
            # TODO: Integrate email/SMS/push API here (e.g., Firebase)
            
        elif kind == "start":
            print(f"[ALERT] Starting Now: Event {event_id} is beginning! (at {notify_at})")
            # TODO: Trigger start-of-event logic here