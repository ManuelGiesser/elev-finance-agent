from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.service import AIAnalysisService
from app.database.session import get_db
from app.repositories.document_repository import DocumentRepository
from app.repositories.invoice_analysis_repository import (
    InvoiceAnalysisRepository,
)

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

    service = AIAnalysisService()

    result = service.analyze_invoice_text(
        document.ocr_text,
    )

    analysis = InvoiceAnalysisRepository(db).create(
        document_id=document.id,
        result=result,
        engine=service.analyzer.name,
    )

    return {
        "document_id": document.id,
        "filename": document.filename,
        "analysis_id": analysis.id,
        "analysis": result.__dict__,
    }