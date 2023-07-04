from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy import ForeignKey


class UserRole(db.Model):
    __tablename__ = "user_roles"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"))
    role_id = db.Column(UUID(as_uuid=True), ForeignKey("roles.id"))
    created_at = db.Column(db.TIMESTAMP(), nullable=True, default=datetime.utcnow())
    updated_at = db.Column(
        db.TIMESTAMP(),
        nullable=True,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
    )
    deleted_at = db.Column(db.TIMESTAMP(), nullable=True)
