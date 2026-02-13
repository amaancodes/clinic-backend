from app.models.base import BaseModel
from app.core.extensions import db
from app.core.enum import AppointmentStatus

class Appointment(BaseModel):
    __tablename__ = "appointments"

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(
        db.Enum(AppointmentStatus, name="appointment_status", native_enum=True), 
        default=AppointmentStatus.SCHEDULED,
        nullable=False
    )

    doctor = db.relationship("Doctor", backref="appointments")
    patient = db.relationship("User", backref="appointments")
