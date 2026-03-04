import pytest
from datetime import datetime, timedelta
from app.appointments.repository import appointment_repository
from app.appointments.models import Appointment
from app.core.enum import AppointmentStatus

def test_appointment_repo_create(db_session):
    start = datetime(2026, 5, 1, 10, 0)
    end = datetime(2026, 5, 1, 11, 0)
    
    appt = appointment_repository.create(patient_id=10, doctor_id=20, start_time=start, end_time=end)
    db_session.flush()
    
    assert appt.id is not None
    assert appt.patient_id == 10
    assert appt.doctor_id == 20
    assert appt.status == AppointmentStatus.SCHEDULED

def test_appointment_repo_find_conflicting(db_session):
    start1 = datetime(2026, 5, 2, 10, 0)
    end1 = datetime(2026, 5, 2, 11, 0)
    appointment_repository.create(patient_id=11, doctor_id=21, start_time=start1, end_time=end1)
    db_session.flush()
    
    # Conflict: exactly same time
    assert appointment_repository.find_conflicting(21, start1, end1) is True
    
    # Conflict: overlapping
    start2 = datetime(2026, 5, 2, 10, 30)
    end2 = datetime(2026, 5, 2, 11, 30)
    assert appointment_repository.find_conflicting(21, start2, end2) is True
    
    # No conflict: after
    start3 = datetime(2026, 5, 2, 11, 0)
    end3 = datetime(2026, 5, 2, 12, 0)
    assert appointment_repository.find_conflicting(21, start3, end3) is False

def test_appointment_repo_get_for_doctor_and_patient(db_session):
    start = datetime(2026, 5, 3, 10, 0)
    end = datetime(2026, 5, 3, 11, 0)
    
    appt = appointment_repository.create(patient_id=30, doctor_id=40, start_time=start, end_time=end)
    db_session.flush()
    
    doctor_appts = appointment_repository.get_for_doctor(40)
    assert len(doctor_appts) == 1
    assert doctor_appts[0].id == appt.id
    
    patient_appts = appointment_repository.get_for_patient(30)
    assert len(patient_appts) == 1
    assert patient_appts[0].id == appt.id
    
    all_appts = appointment_repository.get_all()
    assert len(all_appts) >= 1
