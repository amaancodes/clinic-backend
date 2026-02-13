from app.appointments.models import Appointment
from app.appointments.repository import appointment_repository
from app.doctors.repository import doctor_repository, availability_repository
from app.core.extensions import db
from datetime import datetime

class AppointmentService:
    @staticmethod
    def book_appointment(patient_id: int, doctor_id: int, start_time: datetime, end_time: datetime) -> Appointment:
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")

        doctor = doctor_repository.get_by_id(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")

        # Doctor must have an availability slot covering this time
        availabilities = availability_repository.get_by_doctor_id(doctor_id)
        is_covered = False
        for slot in availabilities:
            if slot.start_time <= start_time and slot.end_time >= end_time:
                is_covered = True
                break
        
        if not is_covered:
            raise ValueError("Doctor is not available at this time")

        # No conflicting appointment(preventing double bookings)
        if appointment_repository.find_conflicting(doctor_id, start_time, end_time):
            raise ValueError("Doctor is already booked at this time")

        try:
            appointment = appointment_repository.create(patient_id, doctor_id, start_time, end_time)
            db.session.commit()
            return appointment
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def list_appointments(user_role: str, user_id: int):
        if user_role == "admin":
            return appointment_repository.get_all()
        elif user_role == "doctor":
            doctor = doctor_repository.get_by_user_id(user_id)
            if not doctor:
                return []
            return appointment_repository.get_for_doctor(doctor.id)
        else:
            return appointment_repository.get_for_patient(user_id)
