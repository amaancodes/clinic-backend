import pytest
from datetime import datetime
from app.doctors.repository import doctor_repository, availability_repository
from app.doctors.models import Doctor, DoctorAvailability
from app.auth.models import User
from app.core.enum import Role

@pytest.fixture
def mock_user(db_session):
    user = User(name="Dr. Smith", email="smith@example.com", password_hash="pwd", role=Role.doctor)
    db_session.add(user)
    db_session.flush()
    return user

def test_doctor_repository_create(db_session, mock_user):
    doctor = doctor_repository.create(user_id=mock_user.id, specialization="General")
    db_session.flush()
    assert doctor.id is not None
    assert doctor.specialization == "General"

def test_doctor_repository_get_by_id(db_session, mock_user):
    doctor = doctor_repository.create(user_id=mock_user.id, specialization="General")
    db_session.flush()
    
    fetched = doctor_repository.get_by_id(doctor.id)
    assert fetched is not None
    assert fetched.id == doctor.id

def test_doctor_repository_get_by_user_id(db_session, mock_user):
    doctor = doctor_repository.create(user_id=mock_user.id, specialization="General")
    db_session.flush()
    
    fetched = doctor_repository.get_by_user_id(mock_user.id)
    assert fetched is not None
    assert fetched.id == doctor.id

def test_doctor_repository_get_all(db_session, mock_user):
    doctor = doctor_repository.create(user_id=mock_user.id, specialization="General")
    db_session.flush()
    
    docs = doctor_repository.get_all()
    assert len(docs) >= 1
    assert any(d.id == doctor.id for d in docs)

def test_availability_repository_create(db_session, mock_user):
    doctor = doctor_repository.create(user_id=mock_user.id, specialization="General")
    db_session.flush()
    
    start = datetime(2026, 3, 1, 9, 0)
    end = datetime(2026, 3, 1, 10, 0)
    avail = availability_repository.create(doctor.id, start, end)
    db_session.flush()
    
    assert avail.id is not None
    assert avail.doctor_id == doctor.id
    assert avail.start_time == start

def test_availability_repository_get_by_doctor_id(db_session, mock_user):
    doctor = doctor_repository.create(user_id=mock_user.id, specialization="General")
    db_session.flush()
    
    start = datetime(2026, 3, 1, 9, 0)
    end = datetime(2026, 3, 1, 10, 0)
    availability_repository.create(doctor.id, start, end)
    db_session.flush()
    
    avails = availability_repository.get_by_doctor_id(doctor.id)
    assert len(avails) == 1
    assert avails[0].start_time == start
