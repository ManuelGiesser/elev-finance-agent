from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentResponse

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def list_documents(
    db: Session = Depends(get_db),
):
    return DocumentRepository(db).list()


@router.get(
    "/stats",
)
def document_stats(
    db: Session = Depends(get_db),
):
    return DocumentRepository(db).stats()


@router.get(
    "/status/{status}",
    response_model=list[DocumentResponse],
)
def documents_by_status(
    status: str,
    db: Session = Depends(get_db),
):
    return DocumentRepository(db).get_by_status(status)


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = DocumentRepository(db).get(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return document