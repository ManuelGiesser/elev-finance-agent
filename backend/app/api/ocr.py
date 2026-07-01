from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.ocr.service import OCRService
from app.repositories.document_repository import DocumentRepository

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
    document = DocumentRepository(db).get(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return {
        "document_id": document.id,
        "filename": document.filename,
        "status": "download_not_implemented_yet",
        "message": "Next step: download file from Google Drive before OCR.",
    }