from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.database.session import get_db
from app.repositories.document_repository import DocumentRepository
from app.repositories.match_repository import MatchRepository
from app.repositories.transaction_repository import TransactionRepository

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
):
    documents = DocumentRepository(db).stats()
    matches = MatchRepository(db).list()
    transactions = TransactionRepository(db).list()

    return {
        "documents": documents,
        "transactions_total": len(transactions),
        "matches_total": len(matches),
        "matches_by_status": {
            "proposed": len([m for m in matches if m.status == "proposed"]),
            "confirmed": len([m for m in matches if m.status == "confirmed"]),
            "rejected": len([m for m in matches if m.status == "rejected"]),
        },
    }


@router.get("/tasks")
def dashboard_tasks(
    db: Session = Depends(get_db),
):
    document_repository = DocumentRepository(db)
    match_repository = MatchRepository(db)

    new_documents = document_repository.get_by_status("new")
    ocr_done_documents = document_repository.get_by_status("ocr_done")
    matches = match_repository.list()

    return {
        "needs_ocr": len(new_documents),
        "ready_for_ai_analysis": len(ocr_done_documents),
        "proposed_matches": len(
            [m for m in matches if m.status == "proposed"]
        ),
        "confirmed_matches": len(
            [m for m in matches if m.status == "confirmed"]
        ),
        "rejected_matches": len(
            [m for m in matches if m.status == "rejected"]
        ),
    }


@router.get("/system")
def dashboard_system():
    return {
        "project_name": settings.project_name,
        "google_drive_enabled": settings.google_drive_enabled,
        "google_drive_ff_configured": bool(settings.google_drive_ff_folder_id),
        "google_drive_belege_configured": bool(
            settings.google_drive_belege_folder_id
        ),
        "google_credentials_configured": bool(
            settings.google_application_credentials
        ),
        "database_configured": bool(settings.database_url),
        "redis_configured": bool(settings.redis_url),
    }