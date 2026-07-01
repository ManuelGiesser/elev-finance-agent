from app.ai.service import AIAnalysisService
from app.repositories.document_repository import DocumentRepository
from app.repositories.invoice_analysis_repository import (
    InvoiceAnalysisRepository,
)


class AIBatchService:

    def __init__(self, db):
        self.db = db
        self.documents = DocumentRepository(db)
        self.analyses = InvoiceAnalysisRepository(db)
        self.ai = AIAnalysisService()

    def analyze_ocr_done_documents(
        self,
        limit: int = 10,
    ):
        documents = self.documents.get_by_status("ocr_done")[:limit]

        analyzed = 0
        errors = []

        for document in documents:

            try:
                if not document.ocr_text:
                    continue

                result = self.ai.analyze_invoice_text(
                    document.ocr_text,
                )

                self.analyses.create(
                    document_id=document.id,
                    result=result,
                    engine=self.ai.analyzer.name,
                )

                document.status = "analyzed"
                self.db.add(document)
                self.db.commit()

                analyzed += 1

            except Exception as exc:
                errors.append(
                    {
                        "document_id": document.id,
                        "filename": document.filename,
                        "error": str(exc),
                    }
                )

        return {
            "analyzed": analyzed,
            "errors": errors,
        }