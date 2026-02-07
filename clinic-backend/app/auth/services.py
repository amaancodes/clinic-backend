from flask_jwt_extended import create_access_token

from app.auth.models import User, Role
from app.core.extensions import db
from app.core.exceptions import AuthenticationError
from app.core.security import hash_password, verify_password


class AuthService:
    """
    Authentication service.

    Contains all business logic for registering users and issuing JWTs.
    """

    @staticmethod
    def register(email: str, password: str, role: str) -> User:
        user = User(
            email=email,
            password_hash=hash_password(password),
            role=Role(role),
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def login(email: str, password: str) -> str:
        user = User.query.filter_by(email=email).first()
        if not user or not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid credentials")

        token = create_access_token(
            identity={"id": user.id, "role": user.role.value}
        )
        return token

