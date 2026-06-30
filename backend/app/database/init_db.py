from app.models.base import Base
from app.models.domain import (
    Document,
    Match,
    SyncJob,
    Transaction,
    Vendor,
    WorkflowRun,
)
from app.database.session import engine


def init_db() -> None:
    Base.metadata.create_all(bind=engine)