from fastapi import APIRouter, Depends, HTTPException

from app.schemas import AgentChatRequest, ToolDetails
from app.deps import get_agent_service
from app.services.agent_service import AgentService

router = APIRouter(
    prefix="/agent",
    tags=["agent"]
)

@router.post("/")
def run(tool_details: ToolDetails, service: AgentService = Depends(get_agent_service)):
    response = service.run(tool=tool_details.tool, arguments=tool_details.arguments)
    if(tool_details.tool == "create_calendar_event" and not response):
        raise HTTPException(status_code=409, detail="Slot not available")
    elif(tool_details.tool == "get_calendar_event" and not response):
        raise HTTPException(status_code=404, detail="Event Not Found")
    elif(tool_details.tool == "list_calendar_events" and not response):
        return response
    elif(not response):
        raise HTTPException(status_code=400, detail="Bad Request") 
    return response

@router.post("/chat")
def chat(request: AgentChatRequest, service: AgentService = Depends(get_agent_service)):
    response = service.run(tool="list_calendar_events")
    return response