from app.reimbursements.models import Reimbursement
from app.core.extensions import db
from app.core.exceptions import ResourceNotFoundError, AuthorizationError, ValidationError
from app.core.enum import ReimbursementStatus, Role
from app.appointments.models import Appointment

class ReimbursementService:
    @staticmethod
    def create_reimbursement(data, member_id):
        # Verify appointment exists and belongs to member
        appointment = Appointment.query.filter_by(id=data['appointment_id'], patient_id=member_id).first()
        if not appointment:
            raise ResourceNotFoundError("Appointment not found or does not belong to you")
        
        # Check if reimbursement already exists for this appointment
        existing = Reimbursement.query.filter_by(appointment_id=data['appointment_id']).first()
        if existing:
            raise ValidationError("Reimbursement already exists for this appointment")

        reimbursement = Reimbursement(
            amount=data['amount'],
            description=data.get('description'),
            member_id=member_id,
            appointment_id=data['appointment_id'],
            status=ReimbursementStatus.PENDING
        )
        db.session.add(reimbursement)
        db.session.commit()
        return reimbursement

    @staticmethod
    def get_reimbursements(user_id, role):
        if role == Role.admin:
            return Reimbursement.query.all()
        return Reimbursement.query.filter_by(member_id=user_id).all()

    @staticmethod
    def get_reimbursement_by_id(reimbursement_id):
        reimbursement = Reimbursement.query.get(reimbursement_id)
        if not reimbursement:
            raise ResourceNotFoundError("Reimbursement not found")
        return reimbursement

    @staticmethod
    def update_reimbursement_status(reimbursement_id, status):
        reimbursement = ReimbursementService.get_reimbursement_by_id(reimbursement_id)
        reimbursement.status = status
        db.session.commit()
        return reimbursement
