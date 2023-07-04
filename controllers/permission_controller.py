from flask import Blueprint, request, jsonify
from schemas.permission_schema import PermissionSchema, PermissionListSchema
from schemas.pagination_schema import PaginationSchema
from repositories.permission_repository import PermissionRepository
from flask_jwt_extended import *
from datetime import datetime
from common.base_response import BaseResponse
from common.error_response import ErrorResponse
from common.base_response_single import BaseResponseSingle
from middlewares.permission_middleware import permission_required
from sqlalchemy import text

permission_api = Blueprint("permission_api", __name__)
ts = datetime.utcnow()


@permission_api.route("/list", methods=["GET"])
@permission_required("Permission@get_list")
def get_list():
    try:
        perm_repo = PermissionRepository()
        records = perm_repo.get_all()
        modules = perm_repo.get_specific_field_distinct(["module"])
        grouped_data = [
            {"module": module.module, "permissions": []} for module in modules
        ]
        # return jsonify(grouped_data)
        for item in records:
            module = item.module
            permission = {"id": item.id, "name": item.name, "module": module}
            check, index = _check_data_exists(grouped_data, "module", module)
            print(check)
            if check:
                grouped_data[index]["permissions"].append(permission)
        results = PermissionListSchema(many=True).dump(grouped_data)
        res = BaseResponseSingle(
            results, "successfully to retrieved data", 200
        ).serialize()
        return jsonify(res), 200
    except Exception as e:
        if "code" in e.args[0]:
            return ErrorResponse(e.args[0]["message"], e.args[0]["code"]).serialize()
        else:
            return ErrorResponse(str(e), 500).serialize()


def _check_data_exists(data_list, key, value):
    for index, item in enumerate(data_list):
        if item.get(key) == value:
            return True, index
    return False, -1
