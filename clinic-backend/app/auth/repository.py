import logging
from app.auth.models import User
from app.core.extensions import db

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for User database operations."""

    def create(self, name: str, email: str, password_hash: str, role: str) -> User:
        """Create a new user."""
        logger.debug("Creating new user")
        user = User(name=name, email=email, password_hash=password_hash, role=role)
        db.session.add(user)
        return user

    def find_by_email(self, email: str) -> User | None:
        """Find user by email."""
        return User.query.filter_by(email=email).first()

    def find_by_id(self, user_id: int) -> User | None:
        return db.session.get(User, user_id)

    def get_all_users(self, limit=None, offset=None) -> list[User]:
        query = User.query
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query.all()

    def update_role(self, user: User, new_role: str) -> User:
        user.role = new_role
        return user


user_repository = UserRepository()