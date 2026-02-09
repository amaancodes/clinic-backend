from app.auth.services import AuthService
from app.admin.services import AdminService
from app.models.user import Role, User
from app.models.doctor import DoctorProfile
from app.models.department import Department
from app.core.extensions import db


def _auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_admin_onboard_doctor(client, app):
    with app.app_context():
        AuthService.register("Admin User", "admin@example.com", "adminpw", "admin")

    # Login as admin
    admin_login = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "adminpw"},
    )
    admin_token = admin_login.get_json()["access_token"]

    # Onboard doctor
    response = client.post(
        "/admin/doctors",
        json={
            "name": "Dr. Strange",
            "email": "strange@example.com",
            "password": "password123",
            "specialization": "Surgery",
        },
        headers=_auth_header(admin_token),
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["specialization"] == "Surgery"
    assert "id" in data
    assert "user_id" in data

    with app.app_context():
        doctor_user = User.query.filter_by(email="strange@example.com").first()
        assert doctor_user is not None
        assert doctor_user.role == Role.DOCTOR
        assert doctor_user.name == "Dr. Strange"


def test_admin_assign_doctor_to_department(client, app):
    with app.app_context():
        AuthService.register("Admin User 2", "admin2@example.com", "adminpw", "admin")
        dept = AdminService.create_department("Cardiology")
        profile = AdminService.onboard_doctor(
            "Dr. Heart", "heart@example.com", "password123", "Cardiology"
        )
        dept_id = dept.id
        doc_id = profile.id

    # Login as admin
    admin_login = client.post(
        "/auth/login",
        json={"email": "admin2@example.com", "password": "adminpw"},
    )
    admin_token = admin_login.get_json()["access_token"]

    # Assign doctor
    response = client.post(
        f"/admin/doctors/{doc_id}/assign",
        json={"department_id": dept_id},
        headers=_auth_header(admin_token),
    )
    assert response.status_code == 200

    with app.app_context():
        doctor = db.session.get(DoctorProfile, doc_id)
        assert len(doctor.departments) == 1
        assert doctor.departments[0].name == "Cardiology"


def test_non_admin_cannot_onboard(client, app):
    with app.app_context():
        AuthService.register("Member User", "member@example.com", "memberpw", "member")

    # Login as member
    member_login = client.post(
        "/auth/login",
        json={"email": "member@example.com", "password": "memberpw"},
    )
    member_token = member_login.get_json()["access_token"]

    # Try to onboard
    response = client.post(
        "/admin/doctors",
        json={
            "name": "Dr. Hack",
            "email": "hack@example.com",
            "password": "password123",
            "specialization": "Hacking",
        },
        headers=_auth_header(member_token),
    )
    assert response.status_code == 403


def test_assign_doctor_invalid_ids(client, app):
    with app.app_context():
        AuthService.register("Admin User 3", "admin3@example.com", "adminpw", "admin")

    # Login as admin
    admin_login = client.post(
        "/auth/login",
        json={"email": "admin3@example.com", "password": "adminpw"},
    )
    admin_token = admin_login.get_json()["access_token"]

    # Assign non-existent doctor
    response = client.post(
        "/admin/doctors/999/assign",
        json={"department_id": 1},
        headers=_auth_header(admin_token),
    )
    assert response.status_code == 404
