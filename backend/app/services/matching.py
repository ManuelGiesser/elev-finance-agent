from decimal import Decimal

from app.models.domain import Document, Transaction


class MatchingService:

    def score(
        self,
        transaction: Transaction,
        document: Document,
    ) -> float:
        score = 0.0

        filename = (document.filename or "").lower()
        vendor_text = (transaction.vendor_text or "").lower()
        booking_text = (transaction.booking_text or "").lower()

        if vendor_text and vendor_text in filename:
            score += 0.4

        if booking_text and any(
            word in filename
            for word in booking_text.split()
            if len(word) > 4
        ):
            score += 0.2

        if document.status == "ocr_done":
            score += 0.2

        if transaction.amount and isinstance(transaction.amount, Decimal):
            score += 0.1

        return min(score, 1.0)