from datetime import datetime
from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class ExampleModel(db.Model):
    __tablename__ = "example"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String())
