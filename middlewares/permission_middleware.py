from functools import wraps
from flask_jwt_extended import *
from repositories.role_permission_repository import RolePermissionRepository
from schemas.role_permission_schema import CheckOrRevokePermissionSchema
from schemas.error_schema import ErrorSchema


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user = get_jwt_identity()
                perm = permission.split("@")
                data = {
                    "user_id": user["id"],
                    "perm_name": perm[1],
                    "module": perm[0],
                }
                data = CheckOrRevokePermissionSchema().load(data)
                check = RolePermissionRepository.CheckPermission(data)
                if check == False:
                    error = ErrorSchema().load(
                        {
                            "message": "You don't have the required permissions to access this resource",
                            "code": 500,
                        }
                    )
                    raise Exception(error)
                # Permission granted, pass the permission value to the route function
                return f(*args, **kwargs)
            except Exception as e:
                error = ErrorSchema().load(
                    {
                        "message": str(e),
                        "code": 500,
                    }
                )
                raise Exception(error)

        return decorated_function

    return decorator
