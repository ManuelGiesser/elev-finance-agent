from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class MatchResponse(BaseModel):
    id: int
    transaction_id: int
    document_id: int
    confidence: Decimal
    match_type: str
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }