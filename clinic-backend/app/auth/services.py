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
    def register(name: str, email: str, password: str, role: str) -> User:
        user = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role=Role(role),
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def login(email: str, password: str) -> tuple[str, int]:
        user = User.query.filter_by(email=email).first()
        if not user or not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid credentials")
        token = create_access_token(
            identity=str(user.id),  
            additional_claims={"role": str(user.role.value)} 
        )
        return token