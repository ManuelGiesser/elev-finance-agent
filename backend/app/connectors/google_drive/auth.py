from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.config.settings import settings


class GoogleDriveAuth:

    @staticmethod
    def service():
        credentials = service_account.Credentials.from_service_account_file(
            settings.google_application_credentials,
            scopes=["https://www.googleapis.com/auth/drive.readonly"],
        )

        return build(
            "drive",
            "v3",
            credentials=credentials,
            cache_discovery=False,
        )