from pathlib import Path

from app.connectors.google_drive.service import GoogleDriveService
from app.ocr.service import OCRService
from app.repositories.document_repository import DocumentRepository


class OCRBatchService:

    def __init__(self, db):
        self.db = db
        self.documents = DocumentRepository(db)
        self.drive = GoogleDriveService()
        self.ocr = OCRService()

    def process_new_documents(
        self,
        limit: int = 10,
    ):
        documents = self.documents.get_by_status("new")[:limit]

        processed = 0
        errors = []

        for document in documents:

            try:
                safe_filename = Path(document.filename).name
                local_path = (
                    f"/tmp/elev-finance-agent/documents/"
                    f"{document.id}_{safe_filename}"
                )

                self.drive.download_file(
                    file_id=document.external_id,
                    target_path=local_path,
                )

                result = self.ocr.extract_text(local_path)

                self.documents.update_ocr_result(
                    document=document,
                    text=result.text,
                    status="ocr_done",
                )

                processed += 1

            except Exception as exc:
                errors.append(
                    {
                        "document_id": document.id,
                        "filename": document.filename,
                        "error": str(exc),
                    }
                )

        return {
            "processed": processed,
            "errors": errors,
        }