import re

from app.ai.base import BaseAIAnalyzer, InvoiceAnalysisResult


class RuleBasedAIAnalyzer(BaseAIAnalyzer):
    name = "rule_based"

    def analyze_invoice_text(self, text: str) -> InvoiceAnalysisResult:
        amount = self._find_amount(text)
        date = self._find_date(text)
        invoice_number = self._find_invoice_number(text)

        return InvoiceAnalysisResult(
            vendor=None,
            invoice_date=date,
            invoice_number=invoice_number,
            total_amount=amount,
            currency="EUR",
            vat_amount=None,
            category="receipt",
            confidence=0.35 if amount or date or invoice_number else 0.1,
        )

    def _find_amount(self, text: str):
        patterns = [
            r"(?i)(gesamt|summe|total|betrag)[^\d]{0,20}(\d+[,.]\d{2})",
            r"(\d+[,.]\d{2})\s?€",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                value = match.groups()[-1]
                return float(value.replace(",", "."))

        return None

    def _find_date(self, text: str):
        match = re.search(r"\b(\d{2}[./-]\d{2}[./-]\d{4})\b", text)
        if match:
            return match.group(1)
        return None

    def _find_invoice_number(self, text: str):
        match = re.search(
            r"(?i)(rechnung|invoice|beleg|receipt)[^\w]{0,10}(nr\.?|nummer|no\.?)?[^\w]{0,10}([A-Z0-9\-\/]+)",
            text,
        )
        if match:
            return match.group(3)
        return None