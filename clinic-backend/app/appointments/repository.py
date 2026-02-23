from app.appointments.models import Appointment
from app.core.enum import AppointmentStatus
from app.core.extensions import db
from datetime import datetime

class AppointmentRepository:
    def create(self, patient_id: int, doctor_id: int, start_time: datetime, end_time: datetime) -> Appointment:
        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            start_time=start_time,
            end_time=end_time,
            status=AppointmentStatus.SCHEDULED
        )
        db.session.add(appointment)
        return appointment

    def find_conflicting(self, doctor_id: int, start_time: datetime, end_time: datetime) -> bool:
        # Check if any appointment overlaps
        # Overlap logic: (StartA < EndB) and (EndA > StartB)
        query = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status != AppointmentStatus.CANCELLED,
            Appointment.start_time < end_time,
            Appointment.end_time > start_time
        )
        return query.first() is not None

    def get_all(self, limit=None, offset=None):
        query = Appointment.query
        if limit is not None:
             query = query.limit(limit)
        if offset is not None:
             query = query.offset(offset)
        return query.all()

    def get_for_doctor(self, doctor_id: int, limit=None, offset=None):
        query = Appointment.query.filter_by(doctor_id=doctor_id)
        if limit is not None:
             query = query.limit(limit)
        if offset is not None:
             query = query.offset(offset)
        return query.all()

    def get_for_patient(self, patient_id: int, limit=None, offset=None):
        query = Appointment.query.filter_by(patient_id=patient_id)
        if limit is not None:
             query = query.limit(limit)
        if offset is not None:
             query = query.offset(offset)
        return query.all()

appointment_repository = AppointmentRepository()
