from fastapi import FastAPI

from app.api.documents import router as documents_router
from app.config.settings import settings
from app.connectors.google_drive.router import (
    router as google_drive_router,
)
from app.database.init_db import init_db

app = FastAPI(
    title=settings.project_name,
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


app.include_router(google_drive_router)
app.include_router(documents_router)