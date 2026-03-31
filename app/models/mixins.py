from datetime import datetime

from app.extensions import db


class SoftDeleteMixin:
    is_deleted = db.Column(db.SmallInteger, nullable=False, default=0, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def soft_delete(self):
        self.is_deleted = 1
        self.deleted_at = datetime.utcnow()

    def restore(self):
        self.is_deleted = 0
        self.deleted_at = None

    @classmethod
    def active_query(cls):
        return cls.query.filter_by(is_deleted=0)


class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
