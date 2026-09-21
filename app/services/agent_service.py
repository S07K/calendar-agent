from datetime import datetime
import json
from app.services.calendar_service import CalendarService
from app.tools.calendar_tools import create_calendar_event, get_calendar_event, list_calendar_events
from openai import OpenAI
from app.config import Settings

class AgentService():
    def __init__(self, calendar_service: CalendarService, settings: Settings) -> None:
        self.tools = {
            "create_calendar_event": create_calendar_event,
            "list_calendar_events": list_calendar_events,
            "get_calendar_event": get_calendar_event,
        }
        self.tool_schema = [
            {
                "type": "function",
                "function": {
                    "name": "create_calendar_event",
                    "description": "Create a calendar events.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string"
                            },
                            "start_time": {
                                "type": "string"
                            },
                            "duration_minutes": {
                                "type": "integer"
                            }
                        },
                        "required": ["title", "start_time", "duration_minutes"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "list_calendar_events",
                    "description": "List all calendar events.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_calendar_event",
                    "description": "Get a calendar events.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "event_id": {
                                "type": "string"
                            }
                        },
                        "required": ["event_id"],
                    },
                },
            },
        ]
        self.calendar_service = calendar_service
        self.client = OpenAI(
            api_key=settings.api_key,
            base_url=settings.base_url,
        )
        self.model=settings.model

    def run(self, tool: str, arguments: dict | None = None):
        fn = self.tools.get(tool)
        arguments = arguments or {}
        if not fn:
            return fn
        return fn(self.calendar_service, **arguments)

    def chat(self, message: str):
        messages = [
            {"role": "system", "content": f"Today is {datetime.now().isoformat()}. Use ISO start_time (YYYY-MM-DDTHH:MM:SS). Prefer tools over guessing."},
            {"role": "user", "content": message}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tool_schema,
            tool_choice="auto"
        )
        assistant_msg = response.choices[0].message
        messages.append(assistant_msg)
        tool_calls = assistant_msg.tool_calls
        if(not tool_calls):
            return None
        tool = tool_calls[0].function.name
        raw = tool_calls[0].function.arguments
        args = json.loads(raw) if(isinstance(raw, str)) else (raw or {})
        result = self.run(tool, args)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_calls[0].id,
            "content": json.dumps(result, default=str)
        })
        followup = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        reply = followup.choices[0].message.content
        return tool, result, reply

