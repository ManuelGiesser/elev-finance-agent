import os


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


class Settings:
    project_name = os.getenv("PROJECT_NAME", "ELEV Finance Agent")
    environment = os.getenv("ENVIRONMENT", "development")
    log_level = os.getenv("LOG_LEVEL", "INFO")

    database_url = os.getenv("DATABASE_URL", "")
    redis_url = os.getenv("REDIS_URL", "")

    google_drive_enabled = env_bool("GOOGLE_DRIVE_ENABLED", True)
    google_drive_ff_folder_id = os.getenv("GOOGLE_DRIVE_FF_FOLDER_ID", "")
    google_drive_belege_folder_id = os.getenv("GOOGLE_DRIVE_BELEGE_FOLDER_ID", "")

    onedrive_enabled = env_bool("ONEDRIVE_ENABLED", False)
    onedrive_tenant_id = os.getenv("ONEDRIVE_TENANT_ID", "")
    onedrive_client_id = os.getenv("ONEDRIVE_CLIENT_ID", "")
    onedrive_client_secret = os.getenv("ONEDRIVE_CLIENT_SECRET", "")
    onedrive_root_folder = os.getenv("ONEDRIVE_ROOT_FOLDER", "")

    hostinger_enabled = env_bool("HOSTINGER_ENABLED", True)
    hostinger_mailbox_id = os.getenv("HOSTINGER_MAILBOX_ID", "")

    openai_api_key = os.getenv("OPENAI_API_KEY", "")


settings = Settings()