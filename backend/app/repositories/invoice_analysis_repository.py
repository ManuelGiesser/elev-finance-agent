from decimal import Decimal

from sqlalchemy.orm import Session

from app.ai.base import InvoiceAnalysisResult
from app.models.domain import InvoiceAnalysis


def to_decimal(value):
    if value is None:
        return None

    return Decimal(str(value))


class InvoiceAnalysisRepository:

    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return (
            self.db.query(InvoiceAnalysis)
            .order_by(InvoiceAnalysis.created_at.desc())
            .all()
        )

    def get_by_document_id(
        self,
        document_id: int,
    ):
        return (
            self.db.query(InvoiceAnalysis)
            .filter(InvoiceAnalysis.document_id == document_id)
            .order_by(InvoiceAnalysis.created_at.desc())
            .all()
        )

    def create(
        self,
        document_id: int,
        result: InvoiceAnalysisResult,
        engine: str,
    ):
        analysis = InvoiceAnalysis(
            document_id=document_id,
            vendor=result.vendor,
            invoice_date=result.invoice_date,
            invoice_number=result.invoice_number,
            total_amount=to_decimal(result.total_amount),
            currency=result.currency,
            vat_amount=to_decimal(result.vat_amount),
            category=result.category,
            confidence=to_decimal(result.confidence),
            engine=engine,
        )

        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)

        return analysis