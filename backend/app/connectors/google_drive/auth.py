from google.oauth2 import service_account
from googleapiclient.discovery import build


class GoogleDriveAuth:

    def __init__(self, credentials_file: str):
        self.credentials_file = credentials_file

    def service(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_file,
            scopes=["https://www.googleapis.com/auth/drive.readonly"],
        )

        return build(
            "drive",
            "v3",
            credentials=credentials,
            cache_discovery=False,
        )