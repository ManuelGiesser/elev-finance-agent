from .auth import GoogleDriveAuth


class GoogleDriveService:

    def __init__(self, credentials_file: str):
        self.drive = GoogleDriveAuth(credentials_file).service()

    def list_files(self, folder_id: str):

        response = (
            self.drive.files()
            .list(
                q=f"'{folder_id}' in parents and trashed=false",
                fields="files(id,name,mimeType,modifiedTime)",
            )
            .execute()
        )

        return response.get("files", [])