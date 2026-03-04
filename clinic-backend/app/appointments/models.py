from app.models.base import BaseModel
from app.core.extensions import db
from app.core.enum import AppointmentStatus
from sqlalchemy.dialects.postgresql import ExcludeConstraint

class Appointment(BaseModel):
    __tablename__ = "appointments"

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False, index=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(
        db.Enum(AppointmentStatus, name="appointment_status", native_enum=True), 
        default=AppointmentStatus.SCHEDULED,
        nullable=False
    )

    doctor = db.relationship("Doctor", back_populates="appointments")
    patient = db.relationship("User", back_populates="appointments")
    reimbursement = db.relationship("Reimbursement", uselist=False, back_populates="appointment")

    __table_args__ = (
        ExcludeConstraint(
            ("doctor_id", "="),
            (db.func.tsrange(db.literal_column("start_time"), db.literal_column("end_time")), "&&"),
            name="prevent_overlapping_appointments",
            where=(db.literal_column("status") != 'CANCELLED')
        ),
    )

    def __repr__(self):
        return f"<Appointment {self.id} - {self.status}>"
