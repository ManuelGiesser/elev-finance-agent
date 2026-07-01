from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.service import AIAnalysisService
from app.database.session import get_db
from app.repositories.document_repository import DocumentRepository

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/documents/{document_id}/analyze")
def analyze_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = DocumentRepository(db).get(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    if not document.ocr_text:
        raise HTTPException(
            status_code=400,
            detail="Document has no OCR text yet.",
        )

    result = AIAnalysisService().analyze_invoice_text(
        document.ocr_text,
    )

    return {
        "document_id": document.id,
        "filename": document.filename,
        "analysis": result.__dict__,
    }