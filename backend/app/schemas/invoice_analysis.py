from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class InvoiceAnalysisResponse(BaseModel):
    id: int
    document_id: int
    vendor: str | None
    invoice_date: str | None
    invoice_number: str | None
    total_amount: Decimal | None
    currency: str | None
    vat_amount: Decimal | None
    category: str | None
    confidence: Decimal | None
    engine: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }