from flask import Blueprint, request, jsonify
from schemas.role_schema import RoleSchema
from schemas.pagination_schema import PaginationSchema
from repositories.role_repository import RoleRepository
from flask_jwt_extended import *
from datetime import datetime
from common.base_response import BaseResponse
from common.error_response import ErrorResponse
from common.base_response_single import BaseResponseSingle
from middlewares.permission_middleware import permission_required

role_api = Blueprint("role_api", __name__)

ts = datetime.utcnow()


@role_api.route("/pagination", methods=["GET"])
@permission_required("Role@get_pagination")
def get_pagination():
    try:
        args = request.args
        query_params = PaginationSchema().load(args)
        roles, count = RoleRepository.get_all_roles(query_params)
        role_schema = RoleSchema(many=True).dump(roles)
        res = BaseResponse(
            role_schema,
            "successfully to retrieved data",
            query_params["page_index"],
            query_params["page_size"],
            count,
            200,
        ).serialize()
        return jsonify(res), 200
    except Exception as e:
        if "code" in e.args[0]:
            return ErrorResponse(e.args[0]["message"], e.args[0]["code"]).serialize()
        else:
            return ErrorResponse(str(e), 500).serialize()


@role_api.route("/list", methods=["GET"])
@permission_required("Role@get_list")
def get_list():
    try:
        records = RoleRepository.get_all()
        results = RoleSchema(many=True).dump(records)
        res = BaseResponseSingle(
            results,
            "successfully to retrieved data",
            200,
        ).serialize()
        return jsonify(res), 200
    except Exception as e:
        if "code" in e.args[0]:
            return ErrorResponse(e.args[0]["message"], e.args[0]["code"]).serialize()
        else:
            return ErrorResponse(str(e), 500).serialize()


@role_api.route("", methods=["POST"])
@permission_required("Role@store")
def store():
    try:
        json = request.json
        role_schema = RoleSchema().load(json)
        role = RoleRepository.create_role(role_schema)
        role = RoleSchema().dump(role)
        res = BaseResponseSingle(role, "successfully to created data!", 201).serialize()
        return jsonify(res), 201
    except Exception as e:
        if "code" in e.args[0]:
            return ErrorResponse(e.args[0]["message"], e.args[0]["code"]).serialize()
        else:
            return ErrorResponse(str(e), 500).serialize()


@role_api.route("/<uuid:id>", methods=["GET"])
@permission_required("Role@get_by_id")
def get_by_id(id):
    try:
        record = RoleRepository.get_role_by_id(id)
        record = RoleSchema().dump(
            record, permissions=record.role_permission.permissions
        )
        res = BaseResponseSingle(
            record, "successfully to retrieved data!", 200
        ).serialize()
        return jsonify(res), 200
    except Exception as e:
        if "code" in e.args[0]:
            return ErrorResponse(e.args[0]["message"], e.args[0]["code"]).serialize()
        else:
            return ErrorResponse(str(e), 500).serialize()


@role_api.route("/<uuid:id>", methods=["PUT"])
@permission_required("Role@update")
def update(id):
    try:
        json = request.json
        role_schema = RoleSchema(partial=True).load(json)
        role = RoleRepository.update_role(id, role_schema)
        role = RoleSchema.dump(role)
        res = BaseResponseSingle(role, "successfully to updated data!", 201).serialize()
        return jsonify(res), 200
    except Exception as e:
        if "code" in e.args[0]:
            return ErrorResponse(e.args[0]["message"], e.args[0]["code"]).serialize()
        else:
            return ErrorResponse(str(e), 500).serialize()


@role_api.route("/<uuid:id>", methods=["DELETE"])
@permission_required("Role@delete")
def delete(id):
    try:
        RoleRepository.deleted_role(id)
        res = BaseResponseSingle(None, "successfully to deleted data!", 201).serialize()
        return jsonify(res), 201
    except Exception as e:
        if "code" in e.args[0]:
            return ErrorResponse(e.args[0]["message"], e.args[0]["code"]).serialize()
        else:
            return ErrorResponse(str(e), 500).serialize()
