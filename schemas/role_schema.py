from marshmallow import Schema, fields, validate, post_dump
from schemas.role_permission_schema import RolePermissionSchema
from schemas.permission_schema import PermissionIdSchema


class RoleSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    slug = fields.String(required=True)
    created_at = fields.Date()
    updated_at = fields.Date()
    deleted_at = fields.Date()
    permission_ids = fields.List(fields.UUID)
    include_permissions = fields.Boolean(default=False, missing=False)

    class Meta:
        strict = True

    @post_dump(pass_many=False)
    def filter_permission_ids(self, data, **kwargs):
        permissions = kwargs.get("permissions")
        if permissions:
            ids = PermissionIdSchema.dump(permissions)
            data["permission_ids"]: ids
        return data


class RoleUpdateSchema(RoleSchema):
    id = fields.UUID(required=True)
    name = fields.String(required=False)
    slug = fields.String(required=False)
