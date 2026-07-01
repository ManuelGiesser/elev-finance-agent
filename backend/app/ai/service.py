from app.ai.base import InvoiceAnalysisResult
from app.ai.rules import RuleBasedAIAnalyzer


class AIAnalysisService:

    def __init__(self):
        self.analyzer = RuleBasedAIAnalyzer()

    def analyze_invoice_text(
        self,
        text: str,
    ) -> InvoiceAnalysisResult:
        return self.analyzer.analyze_invoice_text(text)