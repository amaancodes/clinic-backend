import pytest
from app.reimbursements.services import ReimbursementService
from app.reimbursements.models import Reimbursement
from app.appointments.models import Appointment
from app.core.enum import ReimbursementStatus, Role, AppointmentStatus
from app.core.exceptions import ResourceNotFoundError, ValidationError
from datetime import datetime

@pytest.fixture
def mock_appointment(db_session):
    appt = Appointment(patient_id=1, doctor_id=2, start_time=datetime.now(), end_time=datetime.now(), status=AppointmentStatus.COMPLETED)
    db_session.add(appt)
    db_session.flush()
    return appt

def test_reimbursement_service_create(db_session, mock_appointment):
    data = {
        'appointment_id': mock_appointment.id,
        'amount': 1500.0,
        'description': "Consultation fee"
    }
    reimb = ReimbursementService.create_reimbursement(data, member_id=1)
    
    assert reimb.id is not None
    assert reimb.amount == 1500.0
    assert reimb.status == ReimbursementStatus.PENDING

def test_reimbursement_service_create_invalid_appointment(db_session, mock_appointment):
    data = {
        'appointment_id': 999, # invalid
        'amount': 1500.0
    }
    with pytest.raises(ResourceNotFoundError, match="Appointment not found or does not belong to you"):
        ReimbursementService.create_reimbursement(data, member_id=1)

def test_reimbursement_service_create_duplicate(db_session, mock_appointment):
    data = {
        'appointment_id': mock_appointment.id,
        'amount': 1500.0
    }
    ReimbursementService.create_reimbursement(data, member_id=1)
    
    with pytest.raises(ValidationError, match="Reimbursement already exists for this appointment"):
        ReimbursementService.create_reimbursement(data, member_id=1)

def test_reimbursement_service_get_reimbursements(db_session, mock_appointment):
    data = {'appointment_id': mock_appointment.id, 'amount': 1500.0}
    ReimbursementService.create_reimbursement(data, member_id=1)
    db_session.flush()
    
    admin_list = ReimbursementService.get_reimbursements(user_id=99, role=Role.admin)
    assert len(admin_list) == 1
    
    member_list = ReimbursementService.get_reimbursements(user_id=1, role=Role.member)
    assert len(member_list) == 1
    
    other_member_list = ReimbursementService.get_reimbursements(user_id=2, role=Role.member)
    assert len(other_member_list) == 0

def test_reimbursement_service_update_status(db_session, mock_appointment):
    data = {'appointment_id': mock_appointment.id, 'amount': 1500.0}
    reimb = ReimbursementService.create_reimbursement(data, member_id=1)
    db_session.flush()
    
    updated = ReimbursementService.update_reimbursement_status(reimb.id, ReimbursementStatus.APPROVED)
    assert updated.status == ReimbursementStatus.APPROVED
