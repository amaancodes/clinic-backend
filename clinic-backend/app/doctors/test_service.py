import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.doctors.services import DoctorService
from app.core.constants import ErrorMessages
from app.auth.models import User
from app.doctors.models import Doctor

def test_doctor_service_onboard_doctor_success(db_session):
    doctor = DoctorService.onboard_doctor("Dr. Adams", "adams@example.com", "securepwd", "Pediatrics")
    assert doctor.id is not None
    assert doctor.specialization == "Pediatrics"
    
    user = User.query.get(doctor.user_id)
    assert user is not None
    assert user.email == "adams@example.com"
    assert user.role.value == "doctor"

def test_doctor_service_onboard_doctor_email_exists(db_session):
    DoctorService.onboard_doctor("Dr. Adams", "adams@example.com", "securepwd", "Pediatrics")
    
    with pytest.raises(ValueError, match=ErrorMessages.USER_EMAIL_EXISTS):
        DoctorService.onboard_doctor("Dr. Adams 2", "adams@example.com", "securepwd", "General")

@patch('app.doctors.services.doctor_repository.get_by_id')
@patch('app.doctors.services.department_repository.get_by_id')
def test_doctor_service_assign_department(mock_get_dept, mock_get_doc, db_session):
    mock_doc = MagicMock()
    mock_doc.departments = []
    mock_doc_id = 1
    mock_dept_id = 99
    
    mock_dept = MagicMock()
    
    mock_get_doc.return_value = mock_doc
    mock_get_dept.return_value = mock_dept
    
    DoctorService.assign_department(mock_doc_id, mock_dept_id)
    
    assert mock_dept in mock_doc.departments

def test_doctor_service_set_availability(db_session):
    doctor = DoctorService.onboard_doctor("Dr. Bob", "bob@example.com", "pwd", "ENT")
    
    slot = {
        'start_time': datetime(2026, 4, 1, 10, 0),
        'end_time': datetime(2026, 4, 1, 11, 0)
    }
    
    DoctorService.set_availability(doctor.user_id, [slot])
    
    avails = DoctorService.get_doctor_availability(doctor.id)
    assert len(avails) == 1
    assert avails[0].start_time == slot['start_time']

def test_doctor_service_list_doctors(db_session):
    doctor1 = DoctorService.onboard_doctor("Dr. A", "a@example.com", "pwd", "ENT")
    doctor2 = DoctorService.onboard_doctor("Dr. B", "b@example.com", "pwd", "Urology")
    
    docs = DoctorService.list_doctors()
    names = [d.specialization for d in docs]
    assert "ENT" in names
    assert "Urology" in names
