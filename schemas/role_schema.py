from marshmallow import Schema,fields,validate
from schemas.role_permission_schema import RolePermissionSchema

class RoleSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    slug = fields.String(required=True)
    created_at = fields.Date()
    updated_at = fields.Date()
    deleted_at = fields.Date()
    role_permission = fields.Nested(RolePermissionSchema)
    
    class Meta:
        strict = True
    