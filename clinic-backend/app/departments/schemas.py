from marshmallow import Schema, fields, validate

class DepartmentCreateRequestSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
    )


class DepartmentResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
