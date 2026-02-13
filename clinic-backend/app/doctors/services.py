from app.doctors.models import Doctor, DoctorAvailability
from app.doctors.repository import doctor_repository, availability_repository
from app.departments.repository import department_repository
from app.auth.models import User
from app.core.enum import Role
from app.core.extensions import db
from app.core.security import hash_password
from datetime import datetime

class DoctorService:
    @staticmethod
    def onboard_doctor(name: str, email: str, password: str, specialization: str) -> Doctor:
        # Check if user exists
        if User.query.filter_by(email=email).first():
            raise ValueError("User with this email already exists")

        try:
            # Create User
            user = User(
                name=name,
                email=email,
                password_hash=hash_password(password),
                role=Role.doctor
            )
            db.session.add(user)
            db.session.flush() # Flush to get user.id

            # Create Doctor Profile
            doctor = doctor_repository.create(user_id=user.id, specialization=specialization)
            db.session.commit()
            return doctor
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def assign_department(doctor_id: int, department_id: int):
        doctor = doctor_repository.get_by_id(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        
        department = department_repository.get_by_id(department_id)
        if not department:
            raise ValueError("Department not found")

        try:
            if department not in doctor.departments:
                doctor.departments.append(department)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def set_availability(user_id: int, availabilities: list[dict]):
        doctor = doctor_repository.get_by_user_id(user_id)
        if not doctor:
            raise ValueError("Doctor profile not found")

        try:
            for slot in availabilities:
                availability_repository.create(
                    doctor_id=doctor.id,
                    start_time=slot['start_time'],
                    end_time=slot['end_time']
                )
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_doctor_availability(doctor_id: int) -> list[DoctorAvailability]:
        return availability_repository.get_by_doctor_id(doctor_id)

    @staticmethod
    def list_doctors() -> list[Doctor]:
        return doctor_repository.get_all()
