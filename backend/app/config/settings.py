import os
from dataclasses import dataclass


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    project_name: str = os.getenv("PROJECT_NAME", "ELEV Finance Agent")
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    database_url: str = os.getenv("DATABASE_URL", "")
    redis_url: str = os.getenv("REDIS_URL", "")

    google_drive_enabled: bool = env_bool("GOOGLE_DRIVE_ENABLED")
    google_drive_ff_folder_id: str = os.getenv("GOOGLE_DRIVE_FF_FOLDER_ID", "")
    google_drive_belege_folder_id: str = os.getenv("GOOGLE_DRIVE_BELEGE_FOLDER_ID", "")

    onedrive_enabled: bool = env_bool("ONEDRIVE_ENABLED")
    onedrive_tenant_id: str = os.getenv("ONEDRIVE_TENANT_ID", "")
    onedrive_client_id: str = os.getenv("ONEDRIVE_CLIENT_ID", "")
    onedrive_client_secret: str = os.getenv("ONEDRIVE_CLIENT_SECRET", "")
    onedrive_root_folder: str = os.getenv("ONEDRIVE_ROOT_FOLDER", "")

    hostinger_enabled: bool = env_bool("HOSTINGER_ENABLED")
    hostinger_mailbox_id: str = os.getenv("HOSTINGER_MAILBOX_ID", "")

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")


settings = Settings()
