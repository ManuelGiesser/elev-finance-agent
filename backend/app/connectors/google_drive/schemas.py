from pydantic import BaseModel


class DriveFile(BaseModel):
    id: str
    name: str
    mimeType: str
    modifiedTime: str