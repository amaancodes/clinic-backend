from marshmallow import Schema, fields, validate
from app.core.enum import ReimbursementStatus

class ReimbursementBaseSchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    description = fields.String(required=False, allow_none=True)
    appointment_id = fields.Integer(required=True)

class ReimbursementCreateSchema(ReimbursementBaseSchema):
    pass

class ReimbursementResponseSchema(ReimbursementBaseSchema):
    id = fields.Integer(dump_only=True)
    status = fields.String(dump_only=True)
    member_id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class ReimbursementUpdateSchema(Schema):
    status = fields.String(required=True, validate=validate.OneOf([s.value for s in ReimbursementStatus]))
