from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    full_name = fields.String(required=True)
    nik = fields.String(required=True, validate=validate.Length(min=16, max=16))
    password = (
        fields.String(
            required=True,
            validate=[validate.Length(min=8)],
            load_only=True,
        ),
    )
    pubkey = fields.String(load_only=True)
    privkey = fields.String(load_only=True)
    created_at = fields.String()
    updated_at = fields.String()
    last_login_at = fields.DateTime()
    role = fields.String(required=True)

    class Meta:
        strict = True

    # validate.Regexp("[^a-zA-Z0-9_].")
