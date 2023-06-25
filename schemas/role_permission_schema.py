from marshmallow import Schema, fields, validate
from schema.PermissionSchema import PermissionSchema


class RolePermissionSchema(Schema):
    id = fields.UUID(dump_only=True)
    role_id = fields.UUID()
    permission_id = fields.UUID()
    created_at = fields.Date()
    updated_at = fields.Date()
    deleted_at = fields.Date()
    permission = fields.Nested(PermissionSchema)

    class Meta:
        string = True


class AssignOnePermissionSchema(Schema):
    role_name = fields.String(required=True)
    permission_id = fields.UUID(required=True)


class AssignPermissionsSchema(Schema):
    role_name = fields.String(required=True)
    permission_ids = fields.List(fields.UUID)


class CheckOrRevokePermissionSchema(Schema):
    user_id = fields.UUID(required=True)
    perm_name = fields.String(required=True)
