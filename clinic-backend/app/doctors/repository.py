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

    def get_by_id_with_lock(self, doctor_id: int) -> Doctor | None:
        return Doctor.query.filter_by(id=doctor_id).with_for_update().first()

    def get_by_user_id(self, user_id: int) -> Doctor | None:
        return Doctor.query.filter_by(user_id=user_id).first()

    def get_all(self, limit=None, offset=None) -> list[Doctor]:
        query = Doctor.query
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query.all()

class AvailabilityRepository:
    def create(self, doctor_id: int, start_time: datetime, end_time: datetime) -> DoctorAvailability:
        availability = DoctorAvailability(
            doctor_id=doctor_id, 
            start_time=start_time, 
            end_time=end_time
        )
        db.session.add(availability)
        return availability

    def get_by_doctor_id(self, doctor_id: int, limit=None, offset=None) -> list[DoctorAvailability]:
        query = DoctorAvailability.query.filter_by(doctor_id=doctor_id)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query.all()


doctor_repository = DoctorRepository()
availability_repository = AvailabilityRepository()
