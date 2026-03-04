from app.models.base import BaseModel
from app.core.extensions import db

doctor_departments = db.Table(
    "doctor_departments",
    db.Column("doctor_id", db.Integer, db.ForeignKey("doctors.id")),
    db.Column("department_id", db.Integer, db.ForeignKey("departments.id")),
)

class Doctor(BaseModel):
    __tablename__ = "doctors"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    specialization = db.Column(db.String(100))

    user = db.relationship("User", back_populates="doctor_profile")
    
    departments = db.relationship(
        "Department",
        secondary=doctor_departments,
        back_populates="doctors",
    )

    availabilities = db.relationship("DoctorAvailability", back_populates="doctor", cascade="all, delete-orphan")
    appointments = db.relationship("Appointment", back_populates="doctor")

    def __repr__(self):
        return f"<Doctor {self.id} - {self.specialization}>"

class DoctorAvailability(BaseModel):
    __tablename__ = "doctor_availabilities"

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False, index=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    doctor = db.relationship("Doctor", back_populates="availabilities")

    def __repr__(self):
        return f"<DoctorAvailability {self.id} - {self.doctor_id} ({self.start_time} to {self.end_time})>"
