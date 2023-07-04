from flask.cli import AppGroup
from schemas.permission_schema import PermissionSchema
from schemas.role_permission_schema import AssignPermissionsSchema
from repositories.permission_repository import PermissionRepository
from repositories.role_permission_repository import RolePermissionRepository

permission_commands = AppGroup("permission")


@permission_commands.command("generate")
def route_permission():
    from app import app

    perm_repo = PermissionRepository()
    print("check permission :")
    for rule in app.url_map.iter_rules():
        endpoint = rule.endpoint.split(".")
        if len(endpoint) > 0:
            if "api" in endpoint[0]:
                module = endpoint[0].capitalize().replace("_api", "")
                permission = endpoint[1].capitalize().replace("_", " ")
                slug = endpoint[1]
                print(f"{module}@{permission}")
                if slug != "login" and slug != "register":
                    print("true" if slug != "login" and slug != "register" else "false")
                    datas = [
                        {
                            "field": "slug",
                            "value": slug,
                        },
                        {"field": "module", "value": module},
                    ]
                    check_permission = perm_repo.get_by_multi_field(datas)
                    print("true" if check_permission else "false")
                    if check_permission is None:
                        permission_schema = PermissionSchema().load(
                            {"name": permission, "slug": slug, "module": module}
                        )
                        permission_create = perm_repo.store(schema=permission_schema)
                        print(f"Permission {permission} is succesfully created!")
    permissions = perm_repo.get_all()
    ids = [permission.id for permission in permissions]
    assign_permission = AssignPermissionsSchema().load(
        {"role_name": "Super Admin", "permission_ids": ids}
    )
    print("synchronize permissions to admin")
    RolePermissionRepository.AssignPermission(assign_permission)
    print("synchronize successfully")
