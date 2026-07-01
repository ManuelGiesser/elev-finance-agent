from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.connectors.google_drive.service import GoogleDriveService
from app.database.session import get_db
from app.services.google_drive_sync import GoogleDriveSyncService

router = APIRouter(prefix="/google-drive", tags=["Google Drive"])


@router.get("/status")
def google_drive_status():
    return {
        "enabled": settings.google_drive_enabled,
        "ff_folder_configured": bool(settings.google_drive_ff_folder_id),
        "belege_folder_configured": bool(settings.google_drive_belege_folder_id),
    }


@router.get("/files")
def google_drive_files():
    service = GoogleDriveService()
    return {
        "finanzfluss": service.list_files(settings.google_drive_ff_folder_id),
        "belege": service.list_files(settings.google_drive_belege_folder_id),
    }


@router.post("/sync")
def sync_google_drive(db: Session = Depends(get_db)):
    if not settings.google_drive_enabled:
        raise HTTPException(status_code=400, detail="Google Drive disabled")

    sync = GoogleDriveSyncService(db)

    return {
        "finanzfluss": sync.sync_folder(
            "finanzfluss",
            settings.google_drive_ff_folder_id,
        ),
        "belege": sync.sync_folder(
            "belege",
            settings.google_drive_belege_folder_id,
        ),
    }