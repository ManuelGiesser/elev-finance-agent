from app.ai.base import InvoiceAnalysisResult
from app.ai.mock import MockAIAnalyzer


class AIAnalysisService:

    def __init__(self):
        self.analyzer = MockAIAnalyzer()

    def analyze_invoice_text(
        self,
        text: str,
    ) -> InvoiceAnalysisResult:
        return self.analyzer.analyze_invoice_text(text)