
from app.auth.services import AuthService
from app.doctors.services import DoctorService
from app.core.extensions import db
    
def _auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

def test_list_doctors_includes_name(client, app):
    with app.app_context():
        # Create a doctor
        DoctorService.onboard_doctor(
            "Dr. Strange", "strange@example.com", "password123", "Surgery"
        )
        
        # Create a regular user to browse
        AuthService.register("Regular User", "user@example.com", "userpw")
        
    # Login as regular user
    user_login = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "userpw"},
    )
    token = user_login.get_json()["access_token"]
    
    # List doctors
    response = client.get(
        "/doctors/list",
        headers=_auth_header(token),
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    doctor_data = next((d for d in data if d["name"] == "Dr. Strange"), None)
    assert doctor_data is not None
    assert doctor_data["name"] == "Dr. Strange"
    assert doctor_data["specialization"] == "Surgery"
