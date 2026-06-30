from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)

    source: Mapped[str] = mapped_column(String(100))
    external_id: Mapped[str | None] = mapped_column(String(500))
    folder: Mapped[str | None] = mapped_column(String(100))

    filename: Mapped[str] = mapped_column(String(500))
    mime_type: Mapped[str | None] = mapped_column(String(255))
    file_url: Mapped[str | None] = mapped_column(Text)
    storage_path: Mapped[str | None] = mapped_column(Text)

    size: Mapped[int | None] = mapped_column()

    modified_time: Mapped[datetime | None] = mapped_column(DateTime)

    ocr_status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
    )

    ocr_text: Mapped[str | None] = mapped_column(Text)

    status: Mapped[str] = mapped_column(
        String(50),
        default="new",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    booking_date: Mapped[date | None] = mapped_column(Date)

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        default="EUR",
    )

    account: Mapped[str | None] = mapped_column(String(100))
    counter_account: Mapped[str | None] = mapped_column(String(100))

    vendor_text: Mapped[str | None] = mapped_column(String(500))
    booking_text: Mapped[str | None] = mapped_column(Text)

    status: Mapped[str] = mapped_column(
        String(50),
        default="open",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )


class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
    )

    category: Mapped[str | None] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(String(255))
    website: Mapped[str | None] = mapped_column(String(500))
    invoice_portal: Mapped[str | None] = mapped_column(String(500))
    search_terms: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)

    transaction_id: Mapped[int] = mapped_column(
        ForeignKey("transactions.id")
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id")
    )

    confidence: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
    )

    match_type: Mapped[str] = mapped_column(
        String(100),
        default="automatic",
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="proposed",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )


class SyncJob(Base):
    __tablename__ = "sync_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)

    connector: Mapped[str] = mapped_column(String(100))

    status: Mapped[str] = mapped_column(
        String(50),
        default="running",
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    finished_at: Mapped[datetime | None] = mapped_column(DateTime)

    documents_found: Mapped[int] = mapped_column(default=0)
    errors_count: Mapped[int] = mapped_column(default=0)

    message: Mapped[str | None] = mapped_column(Text)


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id: Mapped[int] = mapped_column(primary_key=True)

    workflow_name: Mapped[str] = mapped_column(String(100))

    status: Mapped[str] = mapped_column(
        String(50),
        default="running",
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    finished_at: Mapped[datetime | None] = mapped_column(DateTime)

    message: Mapped[str | None] = mapped_column(Text)