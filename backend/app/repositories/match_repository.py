from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.domain import Match


class MatchRepository:

    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return (
            self.db.query(Match)
            .order_by(Match.created_at.desc())
            .all()
        )

    def get_by_transaction_id(
        self,
        transaction_id: int,
    ):
        return (
            self.db.query(Match)
            .filter(Match.transaction_id == transaction_id)
            .order_by(Match.confidence.desc())
            .all()
        )

    def create(
        self,
        transaction_id: int,
        document_id: int,
        confidence: float,
        match_type: str = "automatic",
        status: str = "proposed",
    ):
        match = Match(
            transaction_id=transaction_id,
            document_id=document_id,
            confidence=Decimal(str(confidence)),
            match_type=match_type,
            status=status,
        )

        self.db.add(match)
        self.db.commit()
        self.db.refresh(match)

        return match