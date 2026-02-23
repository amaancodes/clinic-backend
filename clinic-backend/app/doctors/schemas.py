from marshmallow import Schema, fields, validate, validates, ValidationError

class DoctorOnboardRequestSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
    specialization = fields.String(required=True, validate=validate.Length(min=1))

class DoctorProfileResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(attribute="user.name", dump_only=True)
    user_id = fields.Integer(dump_only=True)
    specialization = fields.String(dump_only=True)
    departments = fields.Nested("DepartmentResponseSchema", many=True, dump_only=True)

class DoctorAssignRequestSchema(Schema):
    department_id = fields.Integer(required=True)

class AvailabilitySchema(Schema):
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)

class DoctorAvailabilityRequestSchema(Schema):
    availabilities = fields.List(fields.Nested(AvailabilitySchema), required=True)

    @validates("availabilities")
    def validate_availabilities(self, value, **kwargs):
        for slot in value:
            if slot['start_time'] >= slot['end_time']:
                raise ValidationError("Start time must be before end time")