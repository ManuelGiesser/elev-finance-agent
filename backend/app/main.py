from fastapi import FastAPI

from app.config.settings import settings
from app.connectors.google_drive.router import (
    router as google_drive_router,
)

app = FastAPI(
    title=settings.project_name,
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(google_drive_router)