from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.ai import router as ai_router
from app.api.dashboard import router as dashboard_router
from app.api.documents import router as documents_router
from app.api.matches import router as matches_router
from app.api.ocr import router as ocr_router
from app.api.transactions import router as transactions_router
from app.api.workflows import router as workflows_router
from app.config.settings import settings
from app.connectors.google_drive.router import (
    router as google_drive_router,
)
from app.database.init_db import init_db

app = FastAPI(
    title=settings.project_name,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://78.46.162.115:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


app.include_router(google_drive_router)
app.include_router(documents_router)
app.include_router(ocr_router)
app.include_router(ai_router)
app.include_router(matches_router)
app.include_router(transactions_router)
app.include_router(dashboard_router)
app.include_router(workflows_router)