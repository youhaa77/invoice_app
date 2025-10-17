from marshmallow import Schema, fields, validate, ValidationError

# Allowed sets for validation
ALLOWED_METHODS = ["cash", "credit", "transfer"]
ALLOWED_STATUSES = ["paid", "pending", "refunded"]

class InvoiceSchema(Schema):
    customer_name = fields.Str(required=True, validate=validate.Length(min=2))
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    currency = fields.Str(required=True, validate=validate.Length(equal=3))
    description = fields.Str(required=False, allow_none=True)
    payment_method = fields.Str(required=True, validate=validate.OneOf(ALLOWED_METHODS))
    payment_status = fields.Str(required=True, validate=validate.OneOf(ALLOWED_STATUSES))