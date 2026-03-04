from marshmallow import Schema, fields, validate, validates, ValidationError
from app.core.enum import AppointmentStatus

class BookAppointmentSchema(Schema):
    doctor_id = fields.Integer(required=True, validate=validate.Range(min=1))
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)

class AppointmentResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    doctor_id = fields.Integer(dump_only=True)
    patient_id = fields.Integer(dump_only=True)
    start_time = fields.DateTime(dump_only=True)
    end_time = fields.DateTime(dump_only=True)
    status = fields.String(dump_only=True, validate=validate.OneOf([s.value for s in AppointmentStatus]))
