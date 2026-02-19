from marshmallow import Schema, fields, validate, validates, ValidationError

class BookAppointmentSchema(Schema):
    doctor_id = fields.Integer(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)

class AppointmentResponseSchema(Schema):
    id = fields.Integer(required=True)
    doctor_id = fields.Integer(required=True)
    patient_id = fields.Integer(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    status = fields.String(required=True)
