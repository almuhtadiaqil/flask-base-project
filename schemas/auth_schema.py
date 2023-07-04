from marshmallow import Schema, fields, validate, validates
from schemas.user_schema import UserSchema
from schemas.error_schema import ErrorSchema


class LoginSchema(Schema):
    nik = fields.String(required=True, validate=validate.Length(min=16, max=16))
    password = fields.String(
        required=True, validate=[validate.Length(min=8)], load_only=True
    )

    class Meta:
        strict = True


class RegisterSchema(Schema):
    full_name = fields.String(required=True)
    email = fields.String(required=True, validate=[validate.Email()])
    nik = fields.String(required=True, validate=[validate.Length(min=16, max=16)])
    password = fields.String(
        required=True, validate=[validate.Length(min=8)], load_only=True
    )


class LoginResponseSchema(Schema):
    access_token = fields.String()
    expiration_time = fields.DateTime()


class ChangePasswordSchema(Schema):
    old_password = fields.String(required=True, validate=validate.Length(min=8))
    new_password = fields.String(required=True, validate=validate.Length(min=8))
    confirm_new_password = fields.String(required=True, validate=validate.Length(min=8))

    @validates("confirm_new_password")
    def validate_confirm_password(self, value, **kwargs):
        password = self.context[
            "new_password"
        ]  # Get the value of the 'password' field from the context
        if value != password:
            error = ErrorSchema().load(
                {"message": "password do not match", "code": 400}
            )
            raise Exception(error)
