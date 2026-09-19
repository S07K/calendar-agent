from datetime import datetime
from email import message
from pydantic import BaseModel

class EventCreate(BaseModel):
    title: str
    start_time: datetime
    duration_minutes: int

class EventResponse(BaseModel):
    id: str
    title: str
    start_time: datetime
    duration_minutes: int

class Notification(BaseModel):
    event_id: str
    notify_at: datetime
    kind: str
    sent: bool

class ToolDetails(BaseModel):
    tool: str
    arguments: dict = {}

class AgentChatRequest(BaseModel):
    message: str