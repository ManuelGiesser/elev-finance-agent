from sqlalchemy.orm import Session

from app.models.domain import Transaction
from app.schemas.transaction import TransactionCreate


class TransactionRepository:

    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return (
            self.db.query(Transaction)
            .order_by(Transaction.created_at.desc())
            .all()
        )

    def get(self, transaction_id: int):
        return self.db.get(Transaction, transaction_id)

    def create(self, data: TransactionCreate):
        transaction = Transaction(**data.model_dump())

        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)

        return transaction