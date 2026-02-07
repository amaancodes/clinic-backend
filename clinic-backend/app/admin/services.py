from app.admin.models import Department, User, Role, DoctorProfile
from app.core.extensions import db
from app.core.security import hash_password


class AdminService:
    """
    Administrative domain service.

    Handles departments, doctor onboarding, and other admin workflows.
    """

    @staticmethod
    def create_department(name: str) -> Department:
        dept = Department(name=name)
        db.session.add(dept)
        db.session.commit()
        return dept

    @staticmethod
    def list_departments():
        return Department.query.all()

    @staticmethod
    def onboard_doctor(email: str, password: str, specialization: str) -> DoctorProfile:
        user = User(
            email=email,
            password_hash=hash_password(password),
            role=Role.DOCTOR,
        )
        db.session.add(user)
        db.session.flush()

        profile = DoctorProfile(
            user_id=user.id,
            specialization=specialization,
        )
        db.session.add(profile)
        db.session.commit()
        return profile

