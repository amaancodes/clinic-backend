from app.reimbursements.models import Reimbursement
from app.core.extensions import db
from datetime import datetime

class ReimbursementRepository:
    def create(self, amount: float, member_id: int, appointment_id: int, status: str, description: str = None) -> Reimbursement:
        reimbursement = Reimbursement(
            amount=amount,
            description=description,
            member_id=member_id,
            appointment_id=appointment_id,
            status=status
        )
        db.session.add(reimbursement)
        return reimbursement

    def get_by_id(self, reimbursement_id: int) -> Reimbursement | None:
        return db.session.get(Reimbursement, reimbursement_id)

    def get_by_appointment_id(self, appointment_id: int) -> Reimbursement | None:
        return Reimbursement.query.filter_by(appointment_id=appointment_id).first()

    def get_by_member_id(self, member_id: int) -> list[Reimbursement]:
        return Reimbursement.query.filter_by(member_id=member_id).all()

    def get_all(self) -> list[Reimbursement]:
        return Reimbursement.query.all()

reimbursement_repository = ReimbursementRepository()
