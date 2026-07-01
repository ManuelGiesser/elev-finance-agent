from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.domain import Document


class DocumentRepository:

    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        limit: int = 100,
        offset: int = 0,
        query: str | None = None,
    ):
        db_query = self.db.query(Document)

        if query:
            search = f"%{query}%"
            db_query = db_query.filter(
                or_(
                    Document.filename.ilike(search),
                    Document.mime_type.ilike(search),
                    Document.folder.ilike(search),
                    Document.status.ilike(search),
                )
            )

        return (
            db_query
            .order_by(Document.modified_time.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get(self, document_id: int):
        return self.db.get(Document, document_id)

    def get_by_external_id(self, external_id: str):
        return (
            self.db.query(Document)
            .filter(Document.external_id == external_id)
            .first()
        )

    def get_by_status(self, status: str):
        return (
            self.db.query(Document)
            .filter(Document.status == status)
            .order_by(Document.modified_time.desc())
            .all()
        )

    def stats(self):
        total = self.db.query(func.count(Document.id)).scalar()

        by_status = (
            self.db.query(
                Document.status,
                func.count(Document.id),
            )
            .group_by(Document.status)
            .all()
        )

        by_folder = (
            self.db.query(
                Document.folder,
                func.count(Document.id),
            )
            .group_by(Document.folder)
            .all()
        )

        return {
            "total": total,
            "status": {
                status: count
                for status, count in by_status
            },
            "folder": {
                folder: count
                for folder, count in by_folder
            },
        }

    def create_if_missing(self, data: dict):

        existing = self.get_by_external_id(
            data["external_id"]
        )

        if existing:
            return existing, False

        document = Document(**data)

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document, True