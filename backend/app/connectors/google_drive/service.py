from pathlib import Path

from googleapiclient.http import MediaIoBaseDownload

from .auth import GoogleDriveAuth


class GoogleDriveService:

    def __init__(self):
        self.drive = GoogleDriveAuth.service()

    def list_files(self, folder_id: str):
        response = (
            self.drive.files()
            .list(
                q=f"'{folder_id}' in parents and trashed=false",
                fields="files(id,name,mimeType,modifiedTime,size)",
                orderBy="modifiedTime desc",
            )
            .execute()
        )

        return response.get("files", [])

    def download_file(
        self,
        file_id: str,
        target_path: str,
    ) -> str:
        target = Path(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)

        request = self.drive.files().get_media(fileId=file_id)

        with target.open("wb") as file_handle:
            downloader = MediaIoBaseDownload(file_handle, request)

            done = False

            while not done:
                _, done = downloader.next_chunk()

        return str(target)