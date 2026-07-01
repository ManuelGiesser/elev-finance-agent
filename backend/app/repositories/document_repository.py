from sqlalchemy.orm import Session

from app.models.domain import Document


class DocumentRepository:

    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return (
            self.db.query(Document)
            .order_by(Document.modified_time.desc())
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