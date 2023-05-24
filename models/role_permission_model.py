from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class RolePermission(db.Model):
    __tablename__ = "role_permissions"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    permission_id = db.Column(UUID(as_uuid=True))
    role_id = db.Column(UUID(as_uuid=True))
    created_at = db.Column(db.TIMESTAMP(), nullable=True, default=datetime.utcnow())
    updated_at = db.Column(
        db.TIMESTAMP(),
        nullable=True,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
    )
    deleted_at = db.Column(db.TIMESTAMP(), nullable=True)
