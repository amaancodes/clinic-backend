from marshmallow import Schema, fields, validate


class DepartmentCreateRequestSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
    )


class DepartmentResponseSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)


class DoctorOnboardRequestSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
    specialization = fields.String(required=True, validate=validate.Length(min=1))


class DoctorProfileResponseSchema(Schema):
    id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    specialization = fields.String(required=True)


class UserResponseSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    role = fields.String(required=True)
    created_at = fields.DateTime(required=True)


class DoctorAssignRequestSchema(Schema):
    department_id = fields.Integer(required=True)
