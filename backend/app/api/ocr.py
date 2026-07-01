from fastapi import APIRouter

from app.ocr.service import OCRService

router = APIRouter(
    prefix="/ocr",
    tags=["OCR"],
)


@router.get("/test")
def test_ocr():
    result = OCRService().extract_text(
        "/tmp/example-document.pdf"
    )

    return {
        "engine": result.engine,
        "confidence": result.confidence,
        "text": result.text,
    }