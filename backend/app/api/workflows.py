from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.database.session import get_db
from app.services.ai_batch import AIBatchService
from app.services.google_drive_sync import GoogleDriveSyncService
from app.services.ocr_batch import OCRBatchService

router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"],
)


@router.post("/daily")
def daily_workflow(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    google_drive = GoogleDriveSyncService(db)

    sync_result = {
        "finanzfluss": google_drive.sync_folder(
            "finanzfluss",
            settings.google_drive_ff_folder_id,
        ),
        "belege": google_drive.sync_folder(
            "belege",
            settings.google_drive_belege_folder_id,
        ),
    }

    ocr_result = OCRBatchService(db).process_new_documents(limit=limit)
    ai_result = AIBatchService(db).analyze_ocr_done_documents(limit=limit)

    return {
        "sync": sync_result,
        "ocr": ocr_result,
        "ai": ai_result,
    }