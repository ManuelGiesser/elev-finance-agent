import os


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.lower() in ("1", "true", "yes", "on")


class Settings:
    project_name = os.getenv("PROJECT_NAME", "ELEV Finance Agent")

    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://elev:bitte_aendern@postgres:5432/elev_finance",
    )

    redis_url = os.getenv(
        "REDIS_URL",
        "redis://redis:6379/0",
    )

    google_drive_enabled = env_bool("GOOGLE_DRIVE_ENABLED", True)

    google_drive_ff_folder_id = os.getenv(
        "GOOGLE_DRIVE_FF_FOLDER_ID",
        "",
    )

    google_drive_belege_folder_id = os.getenv(
        "GOOGLE_DRIVE_BELEGE_FOLDER_ID",
        "",
    )

    google_application_credentials = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS",
        "/app/secrets/google-service-account.json",
    )


settings = Settings()