from app.auth.services import AuthService
from app.departments.services import DepartmentService
from app.doctors.services import DoctorService
from app.auth.models import Role, User
from app.doctors.models import Doctor
from app.departments.models import Department
from app.core.extensions import db


def _auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _create_admin(name="Admin User", email="admin@example.com", password="adminpw"):
    user = AuthService.register(name, email, password)
    # Manually promote to admin
    user.role = Role.ADMIN
    db.session.commit()
    return user


def test_admin_onboard_doctor(client, app):
    with app.app_context():
        _create_admin()

    # Login as admin
    admin_login = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "adminpw"},
    )
    admin_token = admin_login.get_json()["access_token"]

    # Onboard doctor - POST /doctors/
    response = client.post(
        "/doctors/",
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
        _create_admin("Admin User 2", "admin2@example.com", "adminpw")
        dept = DepartmentService.create_department("Cardiology")
        # Direct service call to create doctor for setup
        profile = DoctorService.onboard_doctor(
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

    # Assign doctor - PUT /doctors/{id}/assign
    response = client.put(
        f"/doctors/{doc_id}/assign",
        json={"department_id": dept_id},
        headers=_auth_header(admin_token),
    )
    assert response.status_code == 200

    with app.app_context():
        doctor = db.session.get(Doctor, doc_id)
        assert len(doctor.departments) == 1
        assert doctor.departments[0].name == "Cardiology"


def test_non_admin_cannot_onboard(client, app):
    with app.app_context():
        AuthService.register("Member User", "member@example.com", "memberpw")

    # Login as member
    member_login = client.post(
        "/auth/login",
        json={"email": "member@example.com", "password": "memberpw"},
    )
    member_token = member_login.get_json()["access_token"]

    # Try to onboard - POST /doctors/
    response = client.post(
        "/doctors/",
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
        _create_admin("Admin User 3", "admin3@example.com", "adminpw")

    # Login as admin
    admin_login = client.post(
        "/auth/login",
        json={"email": "admin3@example.com", "password": "adminpw"},
    )
    admin_token = admin_login.get_json()["access_token"]

    # Assign non-existent doctor
    response = client.put(
        "/doctors/999/assign",
        json={"department_id": 1},
        headers=_auth_header(admin_token),
    )
    # The new service might return 400 with a message if not found inside the try-except logic 
    # or 404 if the route handles it. 
    # Let's check logic: services.py raise ValueError("Doctor not found"). 
    # Routes catch ValueError and return 400.
    # So expected is 400 or 404 depending on how specific we are.
    # Wait, in the route `assign_doctor`: `except ValueError as e: return jsonify({"message": str(e)}), 400`
    assert response.status_code == 400
