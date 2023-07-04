from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(225), unique=True, nullable=False)
    nik = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    pubkey = db.Column(db.Text())
    privkey = db.Column(db.Text())
    last_login_at = db.Column(db.TIMESTAMP(), nullable=True)
    created_at = db.Column(db.TIMESTAMP(), nullable=True, default=datetime.utcnow())
    updated_at = db.Column(
        db.TIMESTAMP(),
        nullable=True,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
    )
    deleted_at = db.Column(db.TIMESTAMP(), nullable=True)
    role = db.relationship("UserRole", backref="users")

    def __init__(
        self,
        full_name,
        email,
        nik,
        password,
        pubkey,
        privkey,
        last_login_at,
    ):
        self.full_name = full_name
        self.email = email
        self.nik = nik
        self.password = password
        self.pubkey = pubkey
        self.privkey = privkey
        self.last_login_at = last_login_at

    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<id {}>".format(self.id)
