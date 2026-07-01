from app.ocr.base import OCRResult
from app.ocr.tesseract import TesseractOCREngine


class OCRService:

    def __init__(self):

        self.engine = TesseractOCREngine()

    def extract_text(
        self,
        file_path: str,
    ) -> OCRResult:

        return self.engine.extract_text(file_path)