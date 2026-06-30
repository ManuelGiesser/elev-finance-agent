from fastapi import APIRouter, HTTPException

from app.config.settings import settings
from app.connectors.google_drive.service import GoogleDriveService

router = APIRouter(
    prefix="/google-drive",
    tags=["Google Drive"],
)


@router.get("/status")
def google_drive_status():
    return {
        "enabled": settings.google_drive_enabled,
        "ff_folder_configured": bool(settings.google_drive_ff_folder_id),
        "belege_folder_configured": bool(settings.google_drive_belege_folder_id),
    }


@router.get("/files")
def google_drive_files():

    if not settings.google_drive_enabled:
        raise HTTPException(
            status_code=400,
            detail="Google Drive connector disabled.",
        )

    service = GoogleDriveService()

    return {
        "finanzfluss": service.list_files(
            settings.google_drive_ff_folder_id
        ),
        "belege": service.list_files(
            settings.google_drive_belege_folder_id
        ),
    }