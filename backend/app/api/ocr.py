from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.connectors.google_drive.service import GoogleDriveService
from app.database.session import get_db
from app.ocr.service import OCRService
from app.repositories.document_repository import DocumentRepository
from app.services.ocr_batch import OCRBatchService

router = APIRouter(
    prefix="/ocr",
    tags=["OCR"],
)


@router.get("/test")
def test_ocr():
    result = OCRService().extract_text(
        "/tmp/example-document.pdf"
    )

    return {
        "engine": result.engine,
        "confidence": result.confidence,
        "text": result.text,
    }


@router.post("/documents/{document_id}")
def ocr_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    repository = DocumentRepository(db)
    document = repository.get(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    safe_filename = Path(document.filename).name
    local_path = (
        f"/tmp/elev-finance-agent/documents/"
        f"{document.id}_{safe_filename}"
    )

    GoogleDriveService().download_file(
        file_id=document.external_id,
        target_path=local_path,
    )

    result = OCRService().extract_text(local_path)

    updated = repository.update_ocr_result(
        document=document,
        text=result.text,
        status="ocr_done",
    )

    return {
        "document_id": updated.id,
        "filename": updated.filename,
        "engine": result.engine,
        "confidence": result.confidence,
        "ocr_status": updated.ocr_status,
        "text_preview": result.text[:500],
    }


@router.post("/batch")
def ocr_batch(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return OCRBatchService(db).process_new_documents(
        limit=limit,
    )