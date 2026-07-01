from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.ai.service import AIAnalysisService
from app.database.session import get_db
from app.repositories.document_repository import DocumentRepository
from app.repositories.invoice_analysis_repository import (
    InvoiceAnalysisRepository,
)
from app.schemas.invoice_analysis import InvoiceAnalysisResponse
from app.services.ai_batch import AIBatchService

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.get(
    "/analyses",
    response_model=list[InvoiceAnalysisResponse],
)
def list_analyses(
    db: Session = Depends(get_db),
):
    return InvoiceAnalysisRepository(db).list()


@router.get(
    "/documents/{document_id}/analyses",
    response_model=list[InvoiceAnalysisResponse],
)
def document_analyses(
    document_id: int,
    db: Session = Depends(get_db),
):
    return InvoiceAnalysisRepository(db).get_by_document_id(
        document_id,
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

    document.status = "analyzed"
    db.add(document)
    db.commit()

    return {
        "document_id": document.id,
        "filename": document.filename,
        "analysis_id": analysis.id,
        "analysis": result.__dict__,
    }


@router.post("/batch")
def analyze_batch(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return AIBatchService(db).analyze_ocr_done_documents(
        limit=limit,
    )