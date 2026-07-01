from app.ai.base import BaseAIAnalyzer, InvoiceAnalysisResult


class MockAIAnalyzer(BaseAIAnalyzer):
    name = "mock"

    def analyze_invoice_text(
        self,
        text: str,
    ) -> InvoiceAnalysisResult:
        return InvoiceAnalysisResult(
            vendor="Unknown",
            category="unclassified",
            confidence=0.0,
        )