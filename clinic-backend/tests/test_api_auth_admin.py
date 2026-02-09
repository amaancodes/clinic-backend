from flask_jwt_extended import decode_token

from app.core.extensions import db
from app.models.user import User, Role
from app.services.auth_service import AuthService


def _auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_register_and_login_flow(client, app):
    # Register a new member via the API
    response = client.post(
        "/auth/register",
        json={
            "name": "API User",
            "email": "apiuser@example.com",
            "password": "pw123",
            "role": "member",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["name"] == "API User"

    # Login via the API
    response = client.post(
        "/auth/login",
        json={"email": "apiuser@example.com", "password": "pw123"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

    # Token should be a valid JWT with minimal identity
    decoded = decode_token(data["access_token"])
    identity = decoded["sub"]
    assert "id" in identity and "role" in identity


def test_register_validation_errors(client):
    # Missing email and too-short password should trigger validation error
    response = client.post(
        "/auth/register",
        json={"name": "Shorty", "password": "short", "role": "member"},
    )
    assert response.status_code == 422
    data = response.get_json()
    assert data.get("error") == "validation_error"
    assert "details" in data
    # Email is required; password must meet length constraints
    assert "email" in data["details"]
    assert "password" in data["details"]


def test_login_validation_errors(client):
    # Missing password should trigger validation error
    response = client.post(
        "/auth/login",
        json={"email": "user@example.com"},
    )
    assert response.status_code == 422
    data = response.get_json()
    assert data.get("error") == "validation_error"
    assert "details" in data
    assert "password" in data["details"]


def test_login_invalid_credentials_returns_401(client):
    # No user created; any login attempt should fail with 401
    response = client.post(
        "/auth/login",
        json={"email": "nosuch@example.com", "password": "bad"},
    )
    assert response.status_code == 401
    data = response.get_json()
    assert data.get("error") == "authentication_error"


def test_admin_department_endpoints_enforce_rbac(client, app):
    with app.app_context():
        # Create an admin and a member using the service layer
        admin = AuthService.register("Admin User", "admin@example.com", "adminpw", "admin")
        member = AuthService.register("Member User", "member@example.com", "memberpw", "member")

        assert admin.role == Role.ADMIN
        assert member.role == Role.MEMBER

    # Login as admin
    admin_login = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "adminpw"},
    )
    admin_token = admin_login.get_json()["access_token"]

    # Login as member
    member_login = client.post(
        "/auth/login",
        json={"email": "member@example.com", "password": "memberpw"},
    )
    member_token = member_login.get_json()["access_token"]

    # Admin can create a department
    create_resp = client.post(
        "/admin/departments",
        json={"name": "Neurology"},
        headers=_auth_header(admin_token),
    )
    assert create_resp.status_code == 200
    dept_data = create_resp.get_json()
    assert "id" in dept_data

    # Admin can list departments
    list_resp = client.get(
        "/admin/departments",
        headers=_auth_header(admin_token),
    )
    assert list_resp.status_code == 200
    departments = list_resp.get_json()
    assert isinstance(departments, list)
    assert any(d["name"] == "Neurology" for d in departments)

    # Non-admin gets forbidden on admin endpoint
    forbidden_resp = client.post(
        "/admin/departments",
        json={"name": "Oncology"},
        headers=_auth_header(member_token),
    )
    assert forbidden_resp.status_code == 403


def test_admin_create_department_validation_error(client, app):
    with app.app_context():
        # Ensure we have an admin user
        AuthService.register("Admin Two", "admin2@example.com", "adminpw", "admin")

    # Login as admin
    admin_login = client.post(
        "/auth/login",
        json={"email": "admin2@example.com", "password": "adminpw"},
    )
    admin_token = admin_login.get_json()["access_token"]

    # Missing name should trigger validation error
    response = client.post(
        "/admin/departments",
        json={},
        headers=_auth_header(admin_token),
    )
    assert response.status_code == 422
    data = response.get_json()
    assert data.get("error") == "validation_error"
    assert "details" in data
    assert "name" in data["details"]


def test_admin_list_users(client, app):
    with app.app_context():
        # Ensure we have users
        AuthService.register("User One", "user1@example.com", "pw123", "member")
        AuthService.register("User Two", "user2@example.com", "pw123", "member")
        # Ensure we have an admin
        AuthService.register("Admin Three", "admin3@example.com", "adminpw", "admin")

    # Login as admin
    admin_login = client.post(
        "/auth/login",
        json={"email": "admin3@example.com", "password": "adminpw"},
    )
    admin_token = admin_login.get_json()["access_token"]

    # List users
    response = client.get(
        "/admin/users",
        headers=_auth_header(admin_token),
    )
    assert response.status_code == 200
    users = response.get_json()
    assert isinstance(users, list)
    assert len(users) >= 3
    assert any(u["name"] == "User One" for u in users)
    assert any(u["role"] == "admin" for u in users)

