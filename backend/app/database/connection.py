import psycopg2
from app.config.settings import settings


def check_database() -> str:
    if not settings.database_url:
        return "missing DATABASE_URL"

    try:
        conn = psycopg2.connect(settings.database_url)
        conn.close()
        return "ok"
    except Exception as exc:
        return f"error: {type(exc).__name__}"
