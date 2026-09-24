import asyncio
from app.logger import Logger
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes.calendar import router as calendar_router
from app.routes.notification import router as notification_router
from app.routes.agent import router as agent_router
from app.deps import get_notification_worker

logger_instance = Logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    notification_worker = get_notification_worker()
    # --- Startup: Start the background worker task ---
    worker_task = asyncio.create_task(notification_worker.start())
    yield
    # --- Shutdown: Cancel the background worker gracefully ---
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

app.include_router(calendar_router)
app.include_router(notification_router)
app.include_router(agent_router)

@app.get("/")
def home():
    return {"message": "Calendar Agent API"}