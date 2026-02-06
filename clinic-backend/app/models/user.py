import enum
from app.models.base import BaseModel
from app.core.extensions import db

class Role(enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    MEMBER = "member"

class User(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
