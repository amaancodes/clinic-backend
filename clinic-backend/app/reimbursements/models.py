from app.models.base import BaseModel
from app.core.extensions import db
from app.core.enum import ReimbursementStatus

class Reimbursement(BaseModel):
    __tablename__ = "reimbursements"

    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(
        db.Enum(ReimbursementStatus, name="reimbursement_status", native_enum=True, values_callable=lambda obj: [e.value for e in obj]),
        default=ReimbursementStatus.PENDING,
        nullable=False
    )
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"), nullable=False, unique=True)

    member = db.relationship("User", back_populates="reimbursements")
    appointment = db.relationship("Appointment", back_populates="reimbursement")
