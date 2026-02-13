from marshmallow import Schema, fields, validate, validates, ValidationError

class BookAppointmentSchema(Schema):
    doctor_id = fields.Integer(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)

    @validates("end_time")
    def validate_end_time(self, value, **kwargs):
        # We need start_time to validate logic, but marshmallow does field validation first.
        # We can implement schema-level validation if needed, or check in service.
        pass

class AppointmentResponseSchema(Schema):
    id = fields.Integer(required=True)
    doctor_id = fields.Integer(required=True)
    patient_id = fields.Integer(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    status = fields.String(required=True)
