from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from models.user_model import User
from schemas.user_schema import UserSchema
from schemas.pagination_schema import PaginationSchema
from schemas.error_schema import ErrorSchema
from common.base_response import BaseResponse
from common.base_response_single import BaseResponseSingle
from common.error_response import ErrorResponse
from repositories.user_repository import UserRepository
from flask_jwt_extended import *
from middlewares.permission_middleware import permission_required

user_api = Blueprint("user_api", __name__)


@user_api.route("/user/pagination", methods=["GET"])
@permission_required("User@get_all_users")
# @swag_from(
#     {
#         "responses": {
#             HTTPStatus.OK.value: {
#                 "description": "Welcome to the Flask Starter Kit",
#                 "schema": UserSchema(many=True),
#             }
#         }
#     }
# )
def get_all_users():
    # user_auth = get_jwt_identity()
    query_params = PaginationSchema()
    args = request.args
    query_params = query_params.load(args)
    try:
        user_schema = UserSchema(many=True)
        users, total = UserRepository.get_all_users(query_params)
        result = user_schema.dump(obj=users.items)
        return jsonify(
            BaseResponse(
                data=result,
                exception="users list",
                limit=query_params["page_size"],
                total=total,
                page=query_params["page_index"],
                status=200,
            ).serialize(),
            200,
        )
    except Exception as e:
        err_schema = ErrorSchema()
        result = err_schema.dump(e)
        if len(e.args[0]) > 1:
            return ErrorResponse(str(e), 400).serialize()
        else:
            return ErrorResponse(e.args[0]["message"], e.args[0]["code"]).serialize()


@user_api.route("/user", methods=["POST"])
@permission_required("User@create_user")
@swag_from(
    {
        "responses": {
            HTTPStatus.OK.value: {
                "description": "Welcome to the Flask Starter Kit",
                "schema": UserSchema(many=True),
            }
        }
    }
)
def create_user():
    user_schema = UserSchema()
    user = user_schema.load(request.json)
    try:
        result = UserRepository.create_user(user)
        return (
            jsonify(
                BaseResponseSingle(
                    user_schema.dump(result), "user created successfully", 201
                ).serialize()
            ),
            201,
        )
    except Exception as e:
        err_schema = ErrorSchema()
        result = err_schema.dump(e)
        if len(e.args[0]) > 1:
            return ErrorResponse(str(e), 400).serialize()
        else:
            return ErrorResponse(e.args[0]["message"], e.args[0]["code"]).serialize()
