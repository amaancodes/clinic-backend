import pytest
from unittest.mock import patch, MagicMock
from app.auth.services import AuthService
from app.auth.models import Role, User
from app.core.exceptions import AuthenticationError, ResourceNotFoundError
from app.core.constants import ErrorMessages

def test_auth_service_register(db_session):
    user = AuthService.register("John Doe", "john@example.com", "mypassword")
    assert user.id is not None
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert user.role == Role.member
    # Verify password was hashed and not plaintext
    assert user.password_hash != "mypassword"

def test_auth_service_login_success(db_session):
    AuthService.register("Jane Doe", "jane@example.com", "secure123")
    db_session.flush()
    
    with patch('app.auth.services.create_access_token') as mock_access, \
         patch('app.auth.services.create_refresh_token') as mock_refresh:
        
        mock_access.return_value = "fake_access"
        mock_refresh.return_value = "fake_refresh"
        
        result = AuthService.login("jane@example.com", "secure123")
        
        assert result["access_token"] == "fake_access"
        assert result["refresh_token"] == "fake_refresh"
        assert result["role"] == Role.member.value

def test_auth_service_login_invalid_password(db_session):
    AuthService.register("Jane Doe", "jane@example.com", "secure123")
    db_session.flush()
    
    with pytest.raises(AuthenticationError, match=ErrorMessages.INVALID_CREDENTIALS):
        AuthService.login("jane@example.com", "wrongpassword")

def test_auth_service_login_invalid_user(db_session):
    with pytest.raises(AuthenticationError, match=ErrorMessages.INVALID_CREDENTIALS):
        AuthService.login("nonexistent@example.com", "password")

def test_auth_service_assign_role(db_session):
    user = AuthService.register("Jane Doe", "jane@example.com", "secure123")
    db_session.flush()
    
    updated = AuthService.assign_role(user.id, Role.admin.value)
    assert updated.role == Role.admin

def test_auth_service_assign_role_not_found(db_session):
    with pytest.raises(ResourceNotFoundError, match=ErrorMessages.USER_NOT_FOUND):
        AuthService.assign_role(999, Role.admin.value)

def test_auth_service_assign_role_invalid_role(db_session):
    user = AuthService.register("Jane Doe", "jane@example.com", "secure123")
    db_session.flush()
    
    with pytest.raises(ValueError, match=ErrorMessages.INVALID_ROLE):
        AuthService.assign_role(user.id, "superadmin_ninja")
