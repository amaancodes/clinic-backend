from app.reimbursements.models import Reimbursement
from app.reimbursements.repository import reimbursement_repository
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
        existing = reimbursement_repository.get_by_appointment_id(data['appointment_id'])
        if existing:
            raise ValidationError("Reimbursement already exists for this appointment")

        try:
            reimbursement = reimbursement_repository.create(
                amount=data['amount'],
                description=data.get('description'),
                member_id=member_id,
                appointment_id=data['appointment_id'],
                status=ReimbursementStatus.PENDING.value
            )
            db.session.commit()
            return reimbursement
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_reimbursements(user_id, role):
        if role == Role.admin:
            return reimbursement_repository.get_all()
        return reimbursement_repository.get_by_member_id(user_id)

    @staticmethod
    def get_reimbursement_by_id(reimbursement_id):
        reimbursement = reimbursement_repository.get_by_id(reimbursement_id)
        if not reimbursement:
            raise ResourceNotFoundError("Reimbursement not found")
        return reimbursement

    @staticmethod
    def update_reimbursement_status(reimbursement_id, status):
        reimbursement = ReimbursementService.get_reimbursement_by_id(reimbursement_id)
        reimbursement.status = status
        try:
            db.session.commit()
            return reimbursement
        except Exception as e:
            db.session.rollback()
            raise e
