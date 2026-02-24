from datetime import datetime

from app.appointments.models import Appointment
from app.appointments.repository import appointment_repository
from app.core.enum import Role
from app.core.extensions import db
from app.doctors.repository import availability_repository, doctor_repository


from abc import ABC, abstractmethod

class AppointmentListingStrategy(ABC):
    @abstractmethod
    def list(self, user_id: int, limit=None, offset=None):
        pass

class AdminListingStrategy(AppointmentListingStrategy):
    def list(self, user_id: int, limit=None, offset=None):
        return appointment_repository.get_all(limit=limit, offset=offset)

class DoctorListingStrategy(AppointmentListingStrategy):
    def list(self, user_id: int, limit=None, offset=None):
        doctor = doctor_repository.get_by_user_id(user_id)
        if not doctor:
            return []
        return appointment_repository.get_for_doctor(doctor.id, limit=limit, offset=offset)

class MemberListingStrategy(AppointmentListingStrategy):
    def list(self, user_id: int, limit=None, offset=None):
        return appointment_repository.get_for_patient(user_id, limit=limit, offset=offset)

from sqlalchemy.exc import IntegrityError
from app.core.constants import ErrorMessages
from app.core.exceptions import ValidationError, ResourceNotFoundError, ConflictError

class AppointmentService:
    @staticmethod
    def book_appointment(patient_id: int, doctor_id: int, start_time: datetime, end_time: datetime) -> Appointment:
        if start_time >= end_time:
            raise ValidationError(ErrorMessages.START_TIME_BEFORE_END_TIME)

        # Use pessimistic lock to prevent concurrent bookings
        doctor = doctor_repository.get_by_id_with_lock(doctor_id)
        if not doctor:
            raise ResourceNotFoundError(ErrorMessages.DOCTOR_NOT_FOUND)

        # Doctor must have an availability slot covering this time
        availabilities = availability_repository.get_by_doctor_id(doctor_id)
        is_covered = False
        for slot in availabilities:
            if slot.start_time <= start_time and slot.end_time >= end_time:
                is_covered = True
                break

        if not is_covered:
            raise ValidationError(ErrorMessages.DOCTOR_UNAVAILABLE)

        # No conflicting appointment(preventing double bookings) - checks existing records
        if appointment_repository.find_conflicting(doctor_id, start_time, end_time):
            raise ConflictError(ErrorMessages.DOCTOR_ALREADY_BOOKED)

        try:
            appointment = appointment_repository.create(patient_id, doctor_id, start_time, end_time)
            db.session.commit()
            return appointment
        except IntegrityError:
            # Fallback for race conditions caught by DB constraint
            db.session.rollback()
            raise ConflictError(ErrorMessages.DOCTOR_ALREADY_BOOKED)
        except Exception as e:
            db.session.rollback()
            raise e

    _STRATEGIES = {
        Role.admin.value: AdminListingStrategy(),
        Role.doctor.value: DoctorListingStrategy(),
        Role.member.value: MemberListingStrategy(),
    }

    @classmethod
    def list_appointments(cls, user_role: str, user_id: int, limit=None, offset=None):
        strategy = cls._STRATEGIES.get(user_role, MemberListingStrategy())
        return strategy.list(user_id, limit=limit, offset=offset)
