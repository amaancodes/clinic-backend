import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from app.appointments.services import AppointmentService
from app.core.constants import ErrorMessages
from app.core.enum import Role
from app.core.exceptions import ValidationError, ResourceNotFoundError, ConflictError

@patch('app.appointments.services.doctor_repository.get_by_id_with_lock')
@patch('app.appointments.services.availability_repository.get_by_doctor_id')
@patch('app.appointments.services.appointment_repository.find_conflicting')
@patch('app.appointments.services.appointment_repository.create')
def test_appointment_service_book_success(mock_create, mock_conflict, mock_get_avail, mock_get_doc, db_session):
    mock_get_doc.return_value = MagicMock(id=1)
    
    # Setup availability that covers the appointment
    mock_avail = MagicMock()
    mock_avail.start_time = datetime(2026, 6, 1, 9, 0)
    mock_avail.end_time = datetime(2026, 6, 1, 17, 0)
    mock_get_avail.return_value = [mock_avail]
    
    mock_conflict.return_value = False
    
    mock_appt = MagicMock(id=100)
    mock_create.return_value = mock_appt
    
    start = datetime(2026, 6, 1, 10, 0)
    end = datetime(2026, 6, 1, 11, 0)
    
    appt = AppointmentService.book_appointment(patient_id=2, doctor_id=1, start_time=start, end_time=end)
    assert appt.id == 100

def test_appointment_service_book_invalid_time():
    start = datetime(2026, 6, 1, 11, 0)
    end = datetime(2026, 6, 1, 10, 0)
    with pytest.raises(ValidationError, match=ErrorMessages.START_TIME_BEFORE_END_TIME):
        AppointmentService.book_appointment(1, 1, start, end)

@patch('app.appointments.services.doctor_repository.get_by_id_with_lock')
def test_appointment_service_book_doctor_not_found(mock_get_doc):
    mock_get_doc.return_value = None
    start = datetime(2026, 6, 1, 10, 0)
    end = datetime(2026, 6, 1, 11, 0)
    with pytest.raises(ResourceNotFoundError, match=ErrorMessages.DOCTOR_NOT_FOUND):
        AppointmentService.book_appointment(1, 999, start, end)

@patch('app.appointments.services.doctor_repository.get_by_id_with_lock')
@patch('app.appointments.services.availability_repository.get_by_doctor_id')
@patch('app.appointments.services.appointment_repository.find_conflicting')
def test_appointment_service_book_conflict(mock_conflict, mock_get_avail, mock_get_doc):
    mock_get_doc.return_value = MagicMock(id=1)
    
    mock_avail = MagicMock()
    mock_avail.start_time = datetime(2026, 6, 1, 9, 0)
    mock_avail.end_time = datetime(2026, 6, 1, 17, 0)
    mock_get_avail.return_value = [mock_avail]
    
    mock_conflict.return_value = True
    
    start = datetime(2026, 6, 1, 10, 0)
    end = datetime(2026, 6, 1, 11, 0)
    
    with pytest.raises(ConflictError, match=ErrorMessages.DOCTOR_ALREADY_BOOKED):
        AppointmentService.book_appointment(1, 1, start, end)

@patch('app.appointments.services.appointment_repository.get_all')
def test_appointment_service_list_admin(mock_get_all):
    AppointmentService.list_appointments(user_role=Role.admin.value, user_id=1)
    mock_get_all.assert_called_once()
