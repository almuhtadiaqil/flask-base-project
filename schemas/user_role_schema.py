from marshmallow import Schema, fields


class UserRoleSchema(Schema):
    id = fields.UUID(dump_only=True)
    user_id = fields.UUID(required=True)
    role_id = fields.UUID(required=True)
    created_at = fields.Date()
    updated_at = fields.Date()
    deleted_at = fields.Date()

    class Meta:
        strict = True


class AssignSingleRole(Schema):
    user_id = fields.UUID()
    role_name = fields.String()

    # class Meta:
    #     strict = True


class AssignBatchRole(Schema):
    user_id = fields.UUID()
    role_names = fields.List(fields.String)

    class Meta:
        strict = True
