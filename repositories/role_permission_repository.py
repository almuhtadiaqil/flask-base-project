from app import db
from models.permission_model import Permission
from models.role_model import Role
from models.role_permission_model import RolePermission
from models.user_role_model import UserRole
from datetime import datetime
from schemas.role_permission_schema import (
    AssignOnePermissionSchema,
    AssignPermissionsSchema,
    CheckOrRevokePermissionSchema,
)
from schemas.error_schema import ErrorSchema

ts = datetime.utcnow()

ErrPermissionNotFound = "Permission not found"
ErrPermissionProhibited = "This role don't have permission to access this"
ErrPermissionAlreadyAssigned = "Permission already assigned to this role"
ErrRoleNotFound = "Role not found"
ErrUserRoleNotFound = "User role not found"


class RolePermissionRepository(db.Model):
    __tablename__ = "role_permission"

    def assignOnePermission(data: AssignOnePermissionSchema):
        try:
            role_name = data.role_name.lower()
            role = Role.query.filter(Role.name.ilike(role_name)).first()
            if role is None:
                error = ErrorSchema().load({"message": ErrRoleNotFound, "code": 400})
                raise Exception(error)
            permission = Permission.query.filter(
                Permission.id == data.permission_id
            ).first()
            if permission is None:
                error = ErrorSchema().load(
                    {"message": ErrPermissionNotFound, "code": 400}
                )
                raise Exception(error)
            role_permission = RolePermission(
                role_id=role.id, permission_id=permission.id
            )
            db.session.add(role_permission)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    def AssignPermission(data: AssignPermissionsSchema):
        try:
            role_name = data.role_name.lower()
            role = Role.query.filter(Role.name.ilike(role_name)).first()
            if role is None:
                error = ErrorSchema().load({"message": ErrRoleNotFound, "code": 400})
                raise Exception(error)
            # perms = []
            for perm_id in data.permission_ids:
                permission = Permission.query.filter(Permission.id == perm_id).first()
                if permission is None:
                    error = ErrorSchema().load(
                        {"message": ErrPermissionNotFound, "code": 400}
                    )
                    raise Exception(error)
                role_perm = RolePermission(role_id=role.id, permission_id=perm_id)
                db.session.add(role_perm)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    def CheckPermission(data: CheckOrRevokePermissionSchema):
        try:
            user_role = UserRole.query.filter(UserRole.user_id == data.user_id).first()
            if user_role is None:
                error = ErrorSchema().load(
                    {"message": ErrUserRoleNotFound, "code": 500}
                )
                raise Exception(error)
            perm_name = data.perm_name.lower()
            permission = Permission.query.filter(
                Permission.name.ilike(perm_name)
            ).first()
            if permission is None:
                error = ErrorSchema().load(
                    {"message": ErrPermissionNotFound, "code": 500}
                )
                raise Exception(error)
            role_permission = RolePermission.query.filter(
                RolePermission.role_id == user_role.role_id,
                RolePermission.permission_id == permission.id,
            ).first()
            if role_permission is None:
                return False
            return True
        except Exception as e:
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    def RevokePermission(data: CheckOrRevokePermissionSchema):
        try:
            user_role = UserRole.query.filter(UserRole.user_id == data.user_id).first()
            if user_role is None:
                error = ErrorSchema().load(
                    {"message": ErrUserRoleNotFound, "code": 500}
                )
                raise Exception(error)
            perm_name = data.perm_name.lower()
            permission = Permission.query.filter(
                Permission.name.ilike(perm_name)
            ).first()
            if permission is None:
                error = ErrorSchema().load(
                    {"message": ErrPermissionNotFound, "code": 500}
                )
                raise Exception(error)
            RolePermission.query.filter(
                RolePermission.role_id == user_role.role_id,
                RolePermission.permission_id == permission.id,
            ).delete()
            return None
        except Exception as e:
            db.session.rollback()
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)
