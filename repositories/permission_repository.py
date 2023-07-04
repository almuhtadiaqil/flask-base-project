from app import db
from models.permission_model import Permission
from models.role_permission_model import RolePermission
from datetime import datetime
from schemas.permission_schema import DeletePermissionSchema, PermissionSchema
from schemas.error_schema import ErrorSchema
from repositories.base_repository import BaseRepository

ErrPermissionInUse = "Cannot delete assigned permission"
ErrPermissionNotFound = "Permission not found"

ts = datetime.utcnow()


class PermissionRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(model=Permission)

    def DeletePermission(data: DeletePermissionSchema):
        try:
            permission_name = data.permission_name.lower()
            permission = Permission.query.filter(
                Permission.name == permission_name
            ).first()
            if permission is None:
                error = ErrorSchema().load(
                    {"message": ErrPermissionNotFound, "code": 500}
                )
                raise Exception(error)
            role_permission = RolePermission.query.filter(
                RolePermission.permission_id == permission.id
            ).first()
            if role_permission != None:
                error = ErrorSchema().load({"message": ErrPermissionInUse, "code": 500})
                raise Exception(error)
            # RolePermission.query.filter(RolePermission.role_id == permission.id).delete()
            permission.deleted_at = ts
            db.commit()
        except Exception as e:
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)
