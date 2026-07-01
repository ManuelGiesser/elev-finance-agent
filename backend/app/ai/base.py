from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class InvoiceAnalysisResult:
    vendor: str | None = None
    invoice_date: str | None = None
    invoice_number: str | None = None
    total_amount: float | None = None
    currency: str | None = "EUR"
    vat_amount: float | None = None
    category: str | None = None
    confidence: float | None = None


class BaseAIAnalyzer(ABC):
    name: str = "base"

    @abstractmethod
    def analyze_invoice_text(
        self,
        text: str,
    ) -> InvoiceAnalysisResult:
        pass