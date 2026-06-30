from fastapi import APIRouter

from app.config.settings import settings

router = APIRouter(prefix="/google-drive", tags=["google-drive"])


@router.get("/status")
def google_drive_status():
    return {
        "enabled": settings.google_drive_enabled,
        "ff_folder_configured": bool(settings.google_drive_ff_folder_id),
        "belege_folder_configured": bool(settings.google_drive_belege_folder_id),
    }


@router.get("/files")
def google_drive_files():
    return {
        "status": "not_connected_yet",
        "message": "Google Drive credentials are not configured yet.",
        "folders": {
            "ff": settings.google_drive_ff_folder_id,
            "belege": settings.google_drive_belege_folder_id,
        },
    }