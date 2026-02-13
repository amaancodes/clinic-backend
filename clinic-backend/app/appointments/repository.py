from app.appointments.models import Appointment
from app.core.enum import AppointmentStatus, Role
from app.core.extensions import db
from sqlalchemy import  and_

class AppointmentRepository:
    def create(self, patient_id: int, doctor_id: int, start_time, end_time) -> Appointment:
        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            start_time=start_time,
            end_time=end_time,
            status=AppointmentStatus.SCHEDULED
        )
        db.session.add(appointment)
        return appointment

    def find_conflicting(self, doctor_id: int, start_time, end_time) -> bool:
        # Check if any appointment overlaps
        # Overlap logic: (StartA < EndB) and (EndA > StartB)
        query = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status != AppointmentStatus.CANCELLED,
            Appointment.start_time < end_time,
            Appointment.end_time > start_time
        )
        return query.first() is not None

    def get_all(self):
        return Appointment.query.all()

    def get_for_doctor(self, doctor_id: int):
        return Appointment.query.filter_by(doctor_id=doctor_id).all()

    def get_for_patient(self, patient_id: int):
        return Appointment.query.filter_by(patient_id=patient_id).all()

appointment_repository = AppointmentRepository()
