from app.models.base import BaseModel
from app.core.extensions import db

doctor_departments = db.Table(
    "doctor_departments",
    db.Column("doctor_id", db.Integer, db.ForeignKey("doctors.id")),
    db.Column("department_id", db.Integer, db.ForeignKey("departments.id")),
)

class Doctor(BaseModel):
    __tablename__ = "doctors"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    specialization = db.Column(db.String(100))

    user = db.relationship("User", backref=db.backref("doctor_profile", uselist=False))
    
    departments = db.relationship(
        "Department",
        secondary=doctor_departments,
        backref="doctors",
    )

class DoctorAvailability(BaseModel):
    __tablename__ = "doctor_availabilities"

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    doctor = db.relationship("Doctor", backref="availabilities")
