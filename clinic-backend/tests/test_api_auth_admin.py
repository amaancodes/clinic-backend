from flask_jwt_extended import decode_token

from app.core.extensions import db
from app.auth.models import User, Role
from app.auth.services import AuthService


def _auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

def _create_admin(name="Admin User", email="admin@example.com", password="adminpw"):
    user = AuthService.register(name, email, password)
    user.role = Role.ADMIN
    db.session.commit()
    return user

def test_register_and_login_flow(client, app):
    response = client.post(
        "/auth/register",
        json={
            "name": "API User",
            "email": "apiuser@example.com",
            "password": "pw123",
            # "role": "member",  
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "user_id" in data

    response = client.post(
        "/auth/login",
        json={"email": "apiuser@example.com", "password": "pw123"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

    decoded = decode_token(data["access_token"])
    identity = decoded["sub"]
    assert identity
    assert "role" in decoded


def test_register_validation_errors(client):
    response = client.post(
        "/auth/register",
        json={"name": "Shorty", "password": "short"},
    )
    assert response.status_code == 422
    data = response.get_json()


def test_login_validation_errors(client):
    response = client.post(
        "/auth/login",
        json={"email": "user@example.com"},
    )
    assert response.status_code in [400, 422]  


def test_login_invalid_credentials_returns_401(client):
    response = client.post(
        "/auth/login",
        json={"email": "nosuch@example.com", "password": "bad"},
    )
    assert response.status_code == 401
    data = response.get_json()
    assert data.get("error") == "authentication_error"


def test_admin_department_endpoints_enforce_rbac(client, app):
    with app.app_context():
        admin = _create_admin()
        member = AuthService.register("Member User", "member@example.com", "memberpw")

    admin_login = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "adminpw"},
    )
    admin_token = admin_login.get_json()["access_token"]

    member_login = client.post(
        "/auth/login",
        json={"email": "member@example.com", "password": "memberpw"},
    )
    member_token = member_login.get_json()["access_token"]

    create_resp = client.post(
        "/departments/",
        json={"name": "Neurology"},
        headers=_auth_header(admin_token),
    )
    assert create_resp.status_code == 201
    dept_data = create_resp.get_json()
    assert "id" in dept_data

    list_resp = client.get(
        "/departments/",
        headers=_auth_header(admin_token),
    )
    assert list_resp.status_code == 200
    departments = list_resp.get_json()
    assert isinstance(departments, list)
    assert any(d["name"] == "Neurology" for d in departments)

    forbidden_resp = client.post(
        "/departments/",
        json={"name": "Oncology"},
        headers=_auth_header(member_token),
    )
    assert forbidden_resp.status_code == 403


def test_admin_create_department_validation_error(client, app):
    with app.app_context():
        _create_admin("Admin Two", "admin2@example.com", "adminpw")

    admin_login = client.post(
        "/auth/login",
        json={"email": "admin2@example.com", "password": "adminpw"},
    )
    admin_token = admin_login.get_json()["access_token"]

    response = client.post(
        "/departments/",
        json={},
        headers=_auth_header(admin_token),
    )
    assert response.status_code in [400, 422]
