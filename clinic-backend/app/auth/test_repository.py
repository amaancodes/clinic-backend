import pytest
from app.auth.repository import user_repository
from app.auth.models import User, Role

def test_user_repository_create(db_session):
    user = user_repository.create(name="Test", email="test@example.com", password_hash="hashed_password", role=Role.member)
    db_session.flush()
    
    assert user.id is not None
    assert user.name == "Test"
    assert user.email == "test@example.com"
    assert user.role == Role.member

def test_user_repository_find_by_email(db_session):
    user_repository.create(name="FindMe", email="findme@example.com", password_hash="pwd", role=Role.member)
    db_session.flush()
    
    fetched = user_repository.find_by_email("findme@example.com")
    assert fetched is not None
    assert fetched.email == "findme@example.com"

def test_user_repository_find_by_id(db_session):
    user = user_repository.create(name="IdUser", email="id@example.com", password_hash="pwd", role=Role.member)
    db_session.flush()
    
    fetched = user_repository.find_by_id(user.id)
    assert fetched is not None
    assert fetched.id == user.id

def test_user_repository_get_all_users(db_session):
    user_repository.create(name="U1", email="u1@example.com", password_hash="pwd", role=Role.member)
    user_repository.create(name="U2", email="u2@example.com", password_hash="pwd", role=Role.member)
    db_session.flush()
    
    users = user_repository.get_all_users()
    assert len(users) >= 2

def test_user_repository_update_role(db_session):
    user = user_repository.create(name="Upgrade", email="upgrade@example.com", password_hash="pwd", role=Role.member)
    db_session.flush()
    
    updated = user_repository.update_role(user, Role.admin)
    db_session.flush()
    
    assert updated.role == Role.admin
