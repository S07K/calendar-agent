from fastapi import FastAPI
from app.routes.calendar import router as calendar_router
from app.routes.notification import router as notification_router
from app.routes.agent import router as agent_router

app = FastAPI()

app.include_router(calendar_router)
app.include_router(notification_router)
app.include_router(agent_router)

@app.get("/")
def home():
    return {"message": "Calendar Agent API"}