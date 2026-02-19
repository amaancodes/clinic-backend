from app.core.enum import Role
from app.models.base import BaseModel
from app.core.extensions import db


class User(BaseModel):
    __tablename__ = "users"

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Role, name="role", native_enum=True), nullable=False)

    appointments = db.relationship("Appointment", back_populates="patient")
    doctor_profile = db.relationship("Doctor", uselist=False, back_populates="user")

    def __repr__(self):
        return f"<User {self.id} - {self.email} ({self.role})>"
