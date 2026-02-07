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
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
    specialization = fields.String(required=True, validate=validate.Length(min=1))


class DoctorProfileResponseSchema(Schema):
    id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    specialization = fields.String(required=True)

