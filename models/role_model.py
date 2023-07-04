from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP(), nullable=True, default=datetime.utcnow())
    updated_at = db.Column(
        db.TIMESTAMP(),
        nullable=True,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
    )
    deleted_at = db.Column(db.TIMESTAMP(), nullable=True)
    role_permission = db.relationship("RolePermission", backref="roles", lazy=True)
