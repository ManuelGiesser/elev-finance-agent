from app.ocr.base import BaseOCREngine, OCRResult


class MockOCREngine(BaseOCREngine):
    name = "mock"

    def extract_text(self, file_path: str) -> OCRResult:
        return OCRResult(
            text=f"Mock OCR text for {file_path}",
            engine=self.name,
            confidence=1.0,
        )