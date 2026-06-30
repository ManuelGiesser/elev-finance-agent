from pydantic import BaseModel


class DocumentCreate(BaseModel):
    source: str
    external_id: str
    folder: str
    filename: str
    mime_type: str | None = None
    size: int | None = None
    modified_time: str | None = None
    status: str = "new"