import pytest

from app.core.extensions import db
from app.core.security import verify_password
from app.core.exceptions import AuthenticationError
from app.models.user import User, Role
from app.services.auth_service import AuthService


def test_register_hashes_password(app):
    with app.app_context():
        user = AuthService.register("member@example.com", "secret", "member")

        persisted = db.session.get(User, user.id)
        assert persisted is not None
        assert persisted.password_hash != "secret"
        assert verify_password("secret", persisted.password_hash)
        assert persisted.role == Role.MEMBER


def test_login_returns_jwt_token(app):
    with app.app_context():
        AuthService.register("user@example.com", "password123", "member")
        token = AuthService.login("user@example.com", "password123")

        assert isinstance(token, str)
        assert token


def test_login_invalid_credentials_raises_authentication_error(app):
    with app.app_context():
        AuthService.register("user2@example.com", "password123", "member")

        with pytest.raises(AuthenticationError):
            AuthService.login("user2@example.com", "wrong-password")

