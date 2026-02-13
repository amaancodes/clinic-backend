import pytest

from app.core.extensions import db
from app.core.security import verify_password
from app.core.exceptions import AuthenticationError
from app.auth.models import User, Role
from app.auth.services import AuthService


def test_register_hashes_password(app):
    with app.app_context():
        # register now only takes name, email, password. Role is default member.
        user = AuthService.register("Member User", "member@example.com", "secret")

        persisted = db.session.get(User, user.id)
        assert persisted is not None
        assert persisted.password_hash != "secret"
        assert verify_password("secret", persisted.password_hash)
        assert persisted.role == Role.member


def test_login_returns_tokens(app):
    with app.app_context():
        AuthService.register("User One", "user@example.com", "password123")
        token_data = AuthService.login("user@example.com", "password123")

        assert isinstance(token_data, dict)
        assert "access_token" in token_data
        assert "refresh_token" in token_data


def test_login_invalid_credentials_raises_authentication_error(app):
    with app.app_context():
        AuthService.register("User Two", "user2@example.com", "password123")

        with pytest.raises(AuthenticationError):
            AuthService.login("user2@example.com", "wrong-password")

