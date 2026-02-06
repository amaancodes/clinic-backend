from app.models.base import BaseModel
from app.core.extensions import db

class DoctorProfile(BaseModel):
    __tablename__ = "doctor_profiles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    specialization = db.Column(db.String(100))

doctor_departments = db.Table(
    "doctor_departments",
    db.Column("doctor_id", db.Integer, db.ForeignKey("doctor_profiles.id")),
    db.Column("department_id", db.Integer, db.ForeignKey("departments.id")),
)
