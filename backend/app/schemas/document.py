from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    source: str
    external_id: str | None
    folder: str | None
    filename: str
    mime_type: str | None
    size: int | None
    status: str
    ocr_status: str
    modified_time: datetime | None

    model_config = {
        "from_attributes": True,
    }


class DocumentDetailResponse(DocumentResponse):
    ocr_text: str | None