from marshmallow import Schema, fields, validate
from user_schema import UserSchema


class LoginSchema(Schema):
    nik = fields.String(required=True, validate=validate.Length(min=16, max=16))
    password = (
        fields.String(
            required=True,
            validate=[validate.Length(min=8)],
            load_only=True,
        ),
    )

    class Meta:
        strict = True


class RegisterSchema(UserSchema):
    role = fields.String(required=False)
