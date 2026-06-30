from fastapi import FastAPI
from app.config.settings import settings
from app.config.logging import setup_logging, logger
from app.database.connection import check_database

setup_logging()

app = FastAPI(title=settings.project_name, version="0.2.0")


@app.on_event("startup")
def on_startup():
    logger.info("Starting %s", settings.project_name)


@app.get("/")
def root():
    return {
        "name": settings.project_name,
        "version": "0.2.0",
        "environment": settings.environment,
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "database": check_database(),
    }


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
