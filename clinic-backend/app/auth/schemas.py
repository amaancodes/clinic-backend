from marshmallow import Schema, fields, validate
from app.core.enum import Role


class RegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class RoleAssignmentSchema(Schema):
    role = fields.Str(
        required=True,
        validate=validate.OneOf([role.value for role in Role])
    )