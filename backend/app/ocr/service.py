from app.ocr.base import OCRResult
from app.ocr.mock import MockOCREngine


class OCRService:
    def __init__(self):
        self.engine = MockOCREngine()

    def extract_text(self, file_path: str) -> OCRResult:
        return self.engine.extract_text(file_path)