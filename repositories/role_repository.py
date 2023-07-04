from models.role_model import Role
from app import db
from datetime import datetime
from schemas.pagination_schema import PaginationSchema
from schemas.role_schema import RoleSchema
from sqlalchemy.sql import text
from schemas.error_schema import ErrorSchema
from datetime import datetime
from repositories.role_permission_repository import RolePermissionRepository
from schemas.role_permission_schema import AssignPermissionsSchema

ts = datetime.utcnow()


class RoleRepository:
    def get_all():
        try:
            records = Role.query.all()
            return records
        except Exception as e:
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    @staticmethod
    def get_all_roles(request: PaginationSchema):
        try:
            query = Role.query.filter(Role.deleted_at == None)
            search = request["search"]
            order_by = request["order_by"]
            page_index = int(request["page_index"])
            page_size = int(request["page_size"])
            if search is not None:
                search = "%{}%".format(search.lower())
                query.filter(Role.name.ilike(search) | Role.slug.ilike(search))
            if order_by is not None:
                order_by = order_by.split(",")
                query.order_by(text("{} {}".format(order_by[0], order_by[1])))
            count = len(query.all())
            result = query.paginate(page_index, page_size)
            return result, count
        except Exception as e:
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    @staticmethod
    def get_role_by_id(id):
        try:
            role = Role.query.filter(Role.id == id, Role.deleted_at == None).first()
            return role
        except Exception as e:
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    @staticmethod
    def create_role(role_schema: RoleSchema):
        try:
            role = Role(
                name=role_schema["name"],
                slug=role_schema["name"].lower().replace(" ", "-"),
            )
            db.session.add(role)
            db.session.commit()
            assign_permission_schema = AssignPermissionsSchema().load(
                {
                    "role_name": role.name,
                    "permission_ids": role_schema["permission_ids"],
                }
            )
            RolePermissionRepository.AssignPermission(assign_permission_schema)
            return role
        except Exception as e:
            db.session.rollback()
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    @staticmethod
    def update_role(id, role_schema: RoleSchema):
        try:
            role = Role.query.filter(Role.id == id).first()
            role.name = role_schema["name"]
            role.slug = role_schema["name"].lower().replace(" ", "-")
            db.session.commit()
            assign_permission_schema = AssignPermissionsSchema().load(
                {
                    "role_name": role.name,
                    "permission_ids": role_schema["permission_ids"],
                }
            )
            RolePermissionRepository.AssignPermission(assign_permission_schema)
            return role
        except Exception as e:
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    @staticmethod
    def deleted_role(id):
        try:
            role = Role.query.get(id)
            if not role:
                error = ErrorSchema().load(
                    {"message": str("role is not found"), "code": 500}
                )
                raise Exception(error)
            db.session.delete(role)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)
