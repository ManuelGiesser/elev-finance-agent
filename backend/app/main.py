from fastapi import FastAPI
from config import settings

app = FastAPI(title=settings.project_name)


@app.get("/")
def root():
    return {
        "name": settings.project_name,
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/config/status")
def config_status():
    return {
        "google_drive_enabled": settings.google_drive_enabled,
        "google_drive_ff_folder_configured": bool(settings.google_drive_ff_folder_id),
        "google_drive_belege_folder_configured": bool(settings.google_drive_belege_folder_id),
        "onedrive_enabled": settings.onedrive_enabled,
        "onedrive_configured": bool(settings.onedrive_tenant_id and settings.onedrive_client_id),
        "hostinger_enabled": settings.hostinger_enabled,
        "hostinger_configured": bool(settings.hostinger_mailbox_id),
        "openai_configured": bool(settings.openai_api_key),
    }