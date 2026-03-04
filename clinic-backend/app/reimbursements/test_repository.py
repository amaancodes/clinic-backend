import pytest
from app.reimbursements.repository import reimbursement_repository
from app.reimbursements.models import Reimbursement
from app.core.enum import ReimbursementStatus

def test_reimbursement_repository_create(db_session):
    reimb = reimbursement_repository.create(
        amount=100.0,
        member_id=1,
        appointment_id=10,
        status=ReimbursementStatus.PENDING.value,
        description="Test desc"
    )
    db_session.flush()
    
    assert reimb.id is not None
    assert reimb.amount == 100.0
    assert reimb.member_id == 1
    assert reimb.appointment_id == 10
    assert reimb.status == ReimbursementStatus.PENDING.value
    assert reimb.description == "Test desc"

def test_reimbursement_repository_get_by_id(db_session):
    reimb = reimbursement_repository.create(
        amount=50.0,
        member_id=2,
        appointment_id=20,
        status=ReimbursementStatus.PENDING.value
    )
    db_session.flush()
    
    fetched = reimbursement_repository.get_by_id(reimb.id)
    assert fetched is not None
    assert fetched.id == reimb.id

def test_reimbursement_repository_get_by_appointment_id(db_session):
    reimb = reimbursement_repository.create(
        amount=50.0,
        member_id=2,
        appointment_id=30,
        status=ReimbursementStatus.PENDING.value
    )
    db_session.flush()
    
    fetched = reimbursement_repository.get_by_appointment_id(30)
    assert fetched is not None
    assert fetched.id == reimb.id
    
    assert reimbursement_repository.get_by_appointment_id(999) is None

def test_reimbursement_repository_get_by_member_id_and_all(db_session):
    reimb1 = reimbursement_repository.create(amount=10.0, member_id=5, appointment_id=40, status=ReimbursementStatus.PENDING.value)
    reimb2 = reimbursement_repository.create(amount=20.0, member_id=5, appointment_id=50, status=ReimbursementStatus.PENDING.value)
    reimb3 = reimbursement_repository.create(amount=30.0, member_id=6, appointment_id=60, status=ReimbursementStatus.PENDING.value)
    db_session.flush()
    
    member_5_reimbs = reimbursement_repository.get_by_member_id(5)
    assert len(member_5_reimbs) == 2
    
    all_reimbs = reimbursement_repository.get_all()
    assert len(all_reimbs) >= 3
