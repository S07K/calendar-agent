from datetime import datetime, timedelta
from typing import Dict

class NotificationService():
    def __init__(self):
        self.notifications: list[Dict] = []

    def get_notifications(self):
        return self.notifications

    def schedule_notification(self, event_id: str, start_time: datetime, kind: str):
        notify_at = start_time
        if(kind == "reminder_5min"):
            notify_at = start_time - timedelta(minutes=5)

        notification = {
            "event_id": event_id,
            "notify_at": notify_at,
            "kind": kind,
            "sent": False
        }
        self.notifications.append(notification)

    def dispatch_due(self, now: datetime):
        notifications_fired = []
        for notification in self.notifications:
            if(notification["notify_at"] <= now and not notification["sent"]):
                notification["sent"] = True
                notifications_fired.append(notification)

        return notifications_fired

        
        