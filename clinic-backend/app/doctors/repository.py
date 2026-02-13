from app.doctors.models import Doctor, DoctorAvailability
from app.core.extensions import db
from datetime import datetime

class DoctorRepository:
    def create(self, user_id: int, specialization: str) -> Doctor:
        doctor = Doctor(user_id=user_id, specialization=specialization)
        db.session.add(doctor)
        return doctor

    def get_by_id(self, doctor_id: int) -> Doctor | None:
        return db.session.get(Doctor, doctor_id)

    def get_by_user_id(self, user_id: int) -> Doctor | None:
        return Doctor.query.filter_by(user_id=user_id).first()

    def get_all(self) -> list[Doctor]:
        return Doctor.query.all()

class AvailabilityRepository:
    def create(self, doctor_id: int, start_time: datetime, end_time: datetime) -> DoctorAvailability:
        availability = DoctorAvailability(
            doctor_id=doctor_id, 
            start_time=start_time, 
            end_time=end_time
        )
        db.session.add(availability)
        return availability

    def get_by_doctor_id(self, doctor_id: int) -> list[DoctorAvailability]:
        return DoctorAvailability.query.filter_by(doctor_id=doctor_id).all()

    def clear_future_availability(self, doctor_id: int):
        # Optional: Strategy to clear old future slots before setting new ones
        # For now, maybe we just append? But "modify availability" usually means "set my schedule".
        # Let's support clearing for simplicity if the user wants to reset.
        # But per request "Only doctors can modify their availability".
        pass

doctor_repository = DoctorRepository()
availability_repository = AvailabilityRepository()
