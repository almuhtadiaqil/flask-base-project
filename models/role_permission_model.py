from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy import ForeignKey


class RolePermission(db.Model):
    __tablename__ = "role_permissions"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    permission_id = db.Column(UUID(as_uuid=True), ForeignKey("permissions.id"))
    role_id = db.Column(UUID(as_uuid=True), ForeignKey("roles.id"))
    created_at = db.Column(db.TIMESTAMP(), nullable=True, default=datetime.utcnow())
    updated_at = db.Column(
        db.TIMESTAMP(),
        nullable=True,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
    )
    deleted_at = db.Column(db.TIMESTAMP(), nullable=True)
    permission = db.relationship("Permission", backref="role_permissions")

    def __init__(self, **kwargs):
        exclude_fields = ["created_at", "updated_at", "deleted_at"]
        for field in exclude_fields:
            kwargs.pop(field, None)
        super(RolePermission, self).__init__(**kwargs)
