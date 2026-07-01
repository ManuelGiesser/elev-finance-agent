from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    booking_date: date | None = None
    amount: Decimal
    currency: str = "EUR"
    account: str | None = None
    counter_account: str | None = None
    vendor_text: str | None = None
    booking_text: str | None = None
    status: str = "open"


class TransactionResponse(TransactionCreate):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }