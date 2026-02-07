from app.core.extensions import db
from app.core.security import verify_password
from app.models.department import Department
from app.models.user import User, Role
from app.services.admin_service import AdminService


def test_create_department_persists_department(app):
    with app.app_context():
        dept = AdminService.create_department("Cardiology")

        persisted = db.session.get(Department, dept.id)
        assert persisted is not None
        assert persisted.name == "Cardiology"


def test_onboard_doctor_hashes_password_and_sets_role(app):
    with app.app_context():
        profile = AdminService.onboard_doctor(
            "doctor@example.com", "strong-password", "Cardiology"
        )

        user = db.session.get(User, profile.user_id)
        assert user is not None
        assert user.email == "doctor@example.com"
        assert user.role == Role.DOCTOR
        assert user.password_hash != "strong-password"
        assert verify_password("strong-password", user.password_hash)

