from app.models.base import BaseModel
from app.core.extensions import db
from app.core.enum import ReimbursementStatus

class Reimbursement(BaseModel):
    __tablename__ = "reimbursements"

    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(
        db.Enum(ReimbursementStatus, name="reimbursement_status", native_enum=True),
        default=ReimbursementStatus.PENDING,
        nullable=False
    )
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"), nullable=False)

    member = db.relationship("User", backref="reimbursements")
    appointment = db.relationship("Appointment", backref="reimbursements")
