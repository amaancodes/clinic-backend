from app.models.department import Department
from app.models.user import User, Role
from app.models.doctor import DoctorProfile
from app.core.extensions import db

class AdminService:

    @staticmethod
    def create_department(name):
        dept = Department(name=name)
        db.session.add(dept)
        db.session.commit()
        return dept

    @staticmethod
    def onboard_doctor(email, password, specialization):
        user = User(
            email=email,
            password_hash=password,
            role=Role.DOCTOR
        )
        db.session.add(user)
        db.session.flush()

        profile = DoctorProfile(
            user_id=user.id,
            specialization=specialization
        )
        db.session.add(profile)
        db.session.commit()
        return profile
