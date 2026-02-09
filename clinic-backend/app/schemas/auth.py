from marshmallow import Schema, fields, validate


class RegisterRequestSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True)
    password = fields.String(required=True)
    role = fields.String(
        required=True,
        validate=validate.OneOf(["admin", "doctor", "member"]),
    )


class RegisterResponseSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    email = fields.Email()
    role = fields.String()


class LoginRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class LoginResponseSchema(Schema):
    access_token = fields.String(required=True)

