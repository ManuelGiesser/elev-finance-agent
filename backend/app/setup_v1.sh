#!/bin/bash
set -e

mkdir -p backend/app/{api,config,connectors/{google_drive,onedrive,hostinger_mail,booking},models,services,database,workflows}
mkdir -p backend/tests dashboard docs db/migrations docker data

cat > docker-compose.yml <<'EOF'
services:
  api:
    build:
      context: ./backend
    container_name: elev_api
    ports:
      - "8000:80"
    env_file:
      - .env
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  postgres:
    image: postgres:16
    container_name: elev_postgres
    environment:
      POSTGRES_DB: elev_finance
      POSTGRES_USER: elev
      POSTGRES_PASSWORD: bitte_aendern
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: elev_redis
    restart: unless-stopped

volumes:
  postgres_data:
EOF

cat > .env.example <<'EOF'
PROJECT_NAME=ELEV Finance Agent
ENVIRONMENT=development
LOG_LEVEL=INFO

DATABASE_URL=postgresql://elev:bitte_aendern@postgres:5432/elev_finance
REDIS_URL=redis://redis:6379/0

GOOGLE_DRIVE_ENABLED=true
GOOGLE_DRIVE_FF_FOLDER_ID=1RVDYcVhd6XIXw3ESVyDxYoJOlvdTao59
GOOGLE_DRIVE_BELEGE_FOLDER_ID=1EJ0GFArYXrWWo6U9SG0f2dAQg4w4rvsZ

ONEDRIVE_ENABLED=false
ONEDRIVE_TENANT_ID=
ONEDRIVE_CLIENT_ID=
ONEDRIVE_CLIENT_SECRET=
ONEDRIVE_ROOT_FOLDER=

HOSTINGER_ENABLED=true
HOSTINGER_MAILBOX_ID=

OPENAI_API_KEY=
EOF

cp .env.example .env

cat > .gitignore <<'EOF'
.env
__pycache__/
*.pyc
*.log
data/
postgres_data/
EOF

cat > backend/Dockerfile <<'EOF'
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
EOF

cat > backend/requirements.txt <<'EOF'
fastapi==0.115.6
uvicorn[standard]==0.34.0
psycopg2-binary==2.9.10
python-dotenv==1.0.1
pydantic==2.10.4
EOF

cat > backend/app/config/settings.py <<'EOF'
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
EOF

cat > backend/app/config/logging.py <<'EOF'
import logging
from .settings import settings


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


logger = logging.getLogger("elev-finance-agent")
EOF

cat > backend/app/database/connection.py <<'EOF'
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
EOF

cat > backend/app/connectors/base.py <<'EOF'
from abc import ABC, abstractmethod


class BaseConnector(ABC):
    name: str = "base"

    @abstractmethod
    def health(self) -> dict:
        raise NotImplementedError
EOF

cat > backend/app/main.py <<'EOF'
from fastapi import FastAPI
from app.config.settings import settings
from app.config.logging import setup_logging, logger
from app.database.connection import check_database

setup_logging()

app = FastAPI(title=settings.project_name, version="1.0.0")


@app.on_event("startup")
def on_startup():
    logger.info("Starting %s", settings.project_name)


@app.get("/")
def root():
    return {
        "name": settings.project_name,
        "version": "1.0.0",
        "environment": settings.environment,
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "database": check_database(),
    }


@app.get("/config/status")
def config_status():
    return {
        "google_drive_enabled": settings.google_drive_enabled,
        "google_drive_ff_folder_configured": bool(settings.google_drive_ff_folder_id),
        "google_drive_belege_folder_configured": bool(settings.google_drive_belege_folder_id),
        "onedrive_enabled": settings.onedrive_enabled,
        "onedrive_configured": bool(settings.onedrive_tenant_id and settings.onedrive_client_id),
        "hostinger_enabled": settings.hostinger_enabled,
        "hostinger_configured": bool(settings.hostinger_mailbox_id),
        "openai_configured": bool(settings.openai_api_key),
    }
EOF

cat > README.md <<'EOF'
# ELEV Finance Agent

## Start

```bash
cp .env.example .env
docker compose up -d --build
curl http://localhost:8000/health
curl http://localhost:8000/config/status