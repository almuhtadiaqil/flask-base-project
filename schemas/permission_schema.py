from marshmallow import Schema, fields


class PermissionSchema(Schema):
    id = fields.UUID()
    name = fields.String()
    slug = fields.String()
    module = fields.String()
    created_at = fields.Date()
    updated_at = fields.Date()
    deleted_at = fields.Date()

    class Meta:
        strict = True


class PermissionListSchema(Schema):
    module = fields.String()
    permissions = fields.Nested(PermissionSchema, many=True)


class PermissionIdSchema(Schema):
    id = fields.UUID()


class DeletePermissionSchema(Schema):
    permission_name = fields.String()
