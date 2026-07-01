from pdf2image import convert_from_path
from PIL import Image
import pytesseract

from app.ocr.base import BaseOCREngine, OCRResult


class TesseractOCREngine(BaseOCREngine):

    name = "tesseract"

    def extract_text(
        self,
        file_path: str,
    ) -> OCRResult:

        if file_path.lower().endswith(".pdf"):

            pages = convert_from_path(file_path)

            text = ""

            for page in pages:
                text += pytesseract.image_to_string(page)

        else:

            image = Image.open(file_path)

            text = pytesseract.image_to_string(image)

        return OCRResult(
            text=text,
            engine=self.name,
            confidence=None,
        )