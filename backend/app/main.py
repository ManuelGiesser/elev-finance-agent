from fastapi import FastAPI

from app.config.settings import settings
from app.connectors.google_drive.connector import GoogleDriveConnector
from app.connectors.registry import registry

app = FastAPI(title=settings.project_name)

registry.register(
    GoogleDriveConnector(
        enabled=settings.google_drive_enabled,
        ff_folder_id=settings.google_drive_ff_folder_id,
        belege_folder_id=settings.google_drive_belege_folder_id,
    )
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/connectors/health")
def connectors_health():
    return [item.__dict__ for item in registry.health()]