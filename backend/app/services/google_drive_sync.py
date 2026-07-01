from datetime import datetime

from app.connectors.google_drive.service import GoogleDriveService
from app.repositories.document_repository import DocumentRepository


def parse_google_time(value: str | None):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


class GoogleDriveSyncService:
    def __init__(self, db):
        self.db = db
        self.drive = GoogleDriveService()
        self.documents = DocumentRepository(db)

    def sync_folder(self, folder_name: str, folder_id: str):
        files = self.drive.list_files(folder_id)
        created = 0

        for file in files:
            _, was_created = self.documents.create_if_missing({
                "source": "google_drive",
                "external_id": file["id"],
                "folder": folder_name,
                "filename": file["name"],
                "mime_type": file.get("mimeType"),
                "size": int(file["size"]) if file.get("size") else None,
                "modified_time": parse_google_time(file.get("modifiedTime")),
                "status": "new",
            })

            if was_created:
                created += 1

        return {
            "folder": folder_name,
            "found": len(files),
            "created": created,
        }