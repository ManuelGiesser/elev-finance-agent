from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.document_repository import DocumentRepository
from app.repositories.match_repository import MatchRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.match import MatchResponse
from app.services.matching import MatchingService

router = APIRouter(
    prefix="/matches",
    tags=["Matches"],
)


@router.get(
    "",
    response_model=list[MatchResponse],
)
def list_matches(
    db: Session = Depends(get_db),
):
    return MatchRepository(db).list()


@router.get(
    "/transaction/{transaction_id}",
    response_model=list[MatchResponse],
)
def matches_for_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    return MatchRepository(db).get_by_transaction_id(
        transaction_id,
    )


@router.post(
    "/suggest/{transaction_id}/{document_id}",
    response_model=MatchResponse,
)
def suggest_match(
    transaction_id: int,
    document_id: int,
    db: Session = Depends(get_db),
):
    transaction = TransactionRepository(db).get(transaction_id)
    document = DocumentRepository(db).get(document_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    confidence = MatchingService().score(
        transaction=transaction,
        document=document,
    )

    return MatchRepository(db).create(
        transaction_id=transaction.id,
        document_id=document.id,
        confidence=confidence,
        match_type="automatic",
        status="proposed",
    )
    confidence = MatchingService().score(
        transaction=transaction,
        document=document,
    )

    return MatchRepository(db).create(
        transaction_id=transaction.id,
        document_id=document.id,
        confidence=confidence,
        match_type="automatic",
        status="proposed",
    )