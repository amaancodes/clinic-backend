from flask_jwt_extended import create_access_token, create_refresh_token

from app.auth.models import User, Role
from app.core.extensions import db
from app.core.exceptions import AuthenticationError, ResourceNotFoundError
from app.core.security import hash_password, verify_password


class AuthService:
    """
    Authentication service.

    Contains all business logic for registering users, issuing JWTs, and managing roles.
    """

    @staticmethod
    def register(name: str, email: str, password: str) -> User:
        user = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role=Role.member,
        )
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def login(email: str, password: str) -> dict:
        user = User.query.filter_by(email=email).first()
        if not user or not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid credentials")
        
        access_token = create_access_token(
            identity=str(user.id),  
            additional_claims={"role": str(user.role.value)} 
        )
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id,
            "role": user.role.value
        }

    @staticmethod
    def assign_role(user_id: int, role_name: str) -> User:
        user = db.session.get(User, user_id)
        if not user:
            raise ResourceNotFoundError("User not found")
        
        try:
            # Validate role
            new_role = Role(role_name)
            user.role = new_role
            db.session.commit()
            return user
        except ValueError:
             # Should be caught by schema validation, but just in case
             raise ValueError("Invalid role")
        except Exception as e:
            db.session.rollback()
            raise e