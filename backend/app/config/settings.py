import os
from dataclasses import dataclass


@dataclass
class Settings:
    project_name: str = os.getenv("PROJECT_NAME", "ELEV Finance Agent")

    database_url: str = os.getenv("DATABASE_URL", "")
    redis_url: str = os.getenv("REDIS_URL", "")

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    google_drive_enabled: bool = os.getenv("GOOGLE_DRIVE_ENABLED", "false").lower() == "true"
    google_drive_ff_folder_id: str = os.getenv("GOOGLE_DRIVE_FF_FOLDER_ID", "")
    google_drive_belege_folder_id: str = os.getenv("GOOGLE_DRIVE_BELEGE_FOLDER_ID", "")

    onedrive_enabled: bool = os.getenv("ONEDRIVE_ENABLED", "false").lower() == "true"
    onedrive_tenant_id: str = os.getenv("ONEDRIVE_TENANT_ID", "")
    onedrive_client_id: str = os.getenv("ONEDRIVE_CLIENT_ID", "")
    onedrive_client_secret: str = os.getenv("ONEDRIVE_CLIENT_SECRET", "")
    onedrive_root_folder: str = os.getenv("ONEDRIVE_ROOT_FOLDER", "")

    hostinger_enabled: bool = os.getenv("HOSTINGER_ENABLED", "false").lower() == "true"
    hostinger_mailbox_id: str = os.getenv("HOSTINGER_MAILBOX_ID", "")


settings = Settings()