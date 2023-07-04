from models.user_model import User
from models.role_model import Role
from models.user_role_model import UserRole
from schemas.user_role_schema import AssignBatchRole, AssignSingleRole
from schemas.error_schema import ErrorSchema
from uuid import UUID
from sqlalchemy import func
from datetime import datetime
from app import db

ts = datetime.utcnow()

ErrRoleAlreadyAssigned = "This role is already assigned to the user"
ErrRoleInUse = "Cannot delete assigned role"
ErrRoleNotFound = "Role not found"
ErrEmptyRole = "Role is empty"
ErrUserRoleNotFound = "User role not found"
ErrUserAlreadyAssigned = "This user is already have role"


class UserRoleRepository:
    def assign_single_role(data: AssignSingleRole):
        try:
            role_name = data["role_name"].lower()
            role = Role.query.filter(
                func.lower(Role.name) == role_name, Role.deleted_at == None
            ).first()
            if role == None:
                role = Role(name=data["role_name"], slug=role_name.replace(" ", "-"))
                db.session.add(role)
                db.session.commit()

            user_role = UserRole.query.filter(
                UserRole.user_id == data["user_id"], UserRole.deleted_at == None
            ).first()
            if user_role is not None:
                error = ErrorSchema().load(
                    {"message": ErrRoleAlreadyAssigned, "code": 500}
                )
                raise Exception(error)

            user_role = UserRole(user_id=data["user_id"], role_id=role.id)
            db.session.add(user_role)
            db.session.commit()
            return user_role
        except Exception as e:
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    def check_assigned_role(data: AssignSingleRole):
        try:
            role_name = data["role_name"].lower()
            role = Role.query.filter(
                Role.name.ilike(role_name), Role.deleted_at == None
            ).first()
            if role == None:
                error = ErrorSchema().load({"message": ErrRoleNotFound, "code": 500})
                raise Exception(error)
            user_role = UserRole.query.filter(
                UserRole.user_id == data["user_id"], UserRole.role_id == role.id
            ).first()
            if user_role == None:
                False
            return True
        except Exception as e:
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    def RevokeRole(data: AssignSingleRole):
        try:
            role_name = data["role_name"].lower()
            role = Role.query.filter(
                Role.name.ilike(role_name), Role.deleted_at == None
            ).first()
            if role == None:
                error = ErrorSchema().load({"message": ErrRoleNotFound, "code": 500})
                raise Exception(error)
            UserRole.query.filter(UserRole.user_id == data["user_id"]).delete()
            db.session.commit()
            return None
        except Exception as e:
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)
