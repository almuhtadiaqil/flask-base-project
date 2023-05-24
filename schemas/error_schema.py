from marshmallow import Schema, fields, validate

class ErrorSchema(Schema):
    message = fields.String()
    code = fields.Integer()