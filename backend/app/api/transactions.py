from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.get(
    "",
    response_model=list[TransactionResponse],
)
def list_transactions(
    db: Session = Depends(get_db),
):
    return TransactionRepository(db).list()


@router.post(
    "",
    response_model=TransactionResponse,
)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
):
    return TransactionRepository(db).create(data)


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    transaction = TransactionRepository(db).get(transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    return transaction