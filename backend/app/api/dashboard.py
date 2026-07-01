from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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