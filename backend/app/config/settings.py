import os


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.lower() in ("1", "true", "yes", "on")


class Settings:

    # Projekt
    project_name = os.getenv(
        "PROJECT_NAME",
        "ELEV Finance Agent",
    )

    # Google Drive
    google_drive_enabled = env_bool(
        "GOOGLE_DRIVE_ENABLED",
        True,
    )

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