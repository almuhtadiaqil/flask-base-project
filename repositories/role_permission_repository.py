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
    __tablename__ = "role_permissions"

    def assignOnePermission(data: AssignOnePermissionSchema):
        try:
            role_name = data["role_name"].lower()
            role = Role.query.filter(Role.name.ilike(role_name)).first()
            if role is None:
                error = ErrorSchema().load({"message": ErrRoleNotFound, "code": 400})
                raise Exception(error)
            permission = Permission.query.filter(
                Permission.id == data.permission_id, Permission
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
            role_name = data["role_name"].lower()
            role = Role.query.filter(Role.name.ilike(role_name)).first()
            if role is None:
                role = Role(
                    name=data["role_name"].lower(),
                    slug=data['role_name'].lower().replace(" ", "-")
                )
                db.session.add(role)
                db.session.commit()
            # perms = []
            for perm_id in data["permission_ids"]:
                permission = Permission.query.filter(Permission.id == perm_id).first()
                if permission is None:
                    error = ErrorSchema().load(
                        {"message": ErrPermissionNotFound, "code": 400}
                    )
                    raise Exception(error)

            exist_perm_ids = (
                RolePermission.query.filter(RolePermission.role_id == role.id)
                .with_entities(RolePermission.permission_id)
                .all()
            )

            exist_perm_ids = [permission_id for (permission_id,) in exist_perm_ids]

            missing_ids = list(set(data["permission_ids"]) - set(exist_perm_ids))
            extra_ids = list(set(exist_perm_ids) - set(data["permission_ids"]))

            for missing_id in missing_ids:
                new_perm = RolePermission(role_id=role.id, permission_id=missing_id)
                db.session.add(new_perm)
            if extra_ids:
                delete_statement = RolePermission.__table__.delete().where(
                    RolePermission.permission_id.in_(extra_ids)
                )
                db.session.execute(delete_statement)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    def CheckPermission(data: CheckOrRevokePermissionSchema):
        try:
            user_role = UserRole.query.filter(
                UserRole.user_id == data["user_id"]
            ).first()
            if user_role is None:
                error = ErrorSchema().load(
                    {"message": ErrUserRoleNotFound, "code": 500}
                )
                raise Exception(error)
            perm_name = data["perm_name"].lower()
            permission = Permission.query.filter(
                Permission.slug.ilike(perm_name), Permission.module == data["module"]
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
            perm_name = data["perm_name"].lower()
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
