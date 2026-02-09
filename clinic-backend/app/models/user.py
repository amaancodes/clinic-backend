import enum
from app.models.base import BaseModel
from app.core.extensions import db

class Role(str, enum.Enum):
    admin = "admin"
    doctor = "doctor"
    user = "user"

class User(BaseModel):
    __tablename__ = "users"

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Role, name="role", native_enum=True), nullable=False)
