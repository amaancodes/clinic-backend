"""Adding indices

Revision ID: dedeb6d32b44
Revises: 122152be5302
Create Date: 2026-02-26 07:46:08.536765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dedeb6d32b44'
down_revision: Union[str, Sequence[str], None] = '122152be5302'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(op.f('ix_appointments_doctor_id'), 'appointments', ['doctor_id'], unique=False)
    op.create_index(op.f('ix_appointments_patient_id'), 'appointments', ['patient_id'], unique=False)
    op.create_unique_constraint(op.f('uq_doctors_user_id'), 'doctors', ['user_id'])
    op.create_index(op.f('ix_doctor_availabilities_doctor_id'), 'doctor_availabilities', ['doctor_id'], unique=False)
    op.create_index(op.f('ix_reimbursements_member_id'), 'reimbursements', ['member_id'], unique=False)
    op.create_unique_constraint(op.f('uq_reimbursements_appointment_id'), 'reimbursements', ['appointment_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f('uq_reimbursements_appointment_id'), 'reimbursements', type_='unique')
    op.drop_index(op.f('ix_reimbursements_member_id'), table_name='reimbursements')
    op.drop_index(op.f('ix_doctor_availabilities_doctor_id'), table_name='doctor_availabilities')
    op.drop_constraint(op.f('uq_doctors_user_id'), 'doctors', type_='unique')
    op.drop_index(op.f('ix_appointments_patient_id'), table_name='appointments')
    op.drop_index(op.f('ix_appointments_doctor_id'), table_name='appointments')
