from flask import Blueprint, request, jsonify
from models.user_model import User
from schemas.user_schema import UserSchema
from schemas.user_role_schema import AssignSingleRole
from schemas.pagination_schema import PaginationSchema
from schemas.error_schema import ErrorSchema
from common.base_response import BaseResponse
from common.base_response_single import BaseResponseSingle
from common.error_response import ErrorResponse
from repositories.user_repository import UserRepository
from repositories.user_role_repository import UserRoleRepository
from flask_jwt_extended import *
from schemas.auth_schema import (
    LoginSchema,
    RegisterSchema,
    LoginResponseSchema,
    ChangePasswordSchema,
)
from flask_jwt_extended.utils import decode_token
from datetime import datetime
from middlewares.permission_middleware import permission_required

auth_api = Blueprint("auth_api", __name__)

ts = datetime.utcnow()


@auth_api.route("/login", methods=["POST"])
def login():
    # request_data = LoginSchema()
    json = request.json
    request_data = LoginSchema().load(json)
    try:
        user = UserRepository.get_user_by_field("nik", request_data["nik"])
        if user is None:
            return ErrorResponse("credentials missmatch!", 400).serialize()
        if user.checkPassword(request_data["password"]) == False:
            return ErrorResponse("credentials missmatch!", 400).serialize()
        user_schema = UserSchema()
        user_schema = user_schema.dump(user)
        login_response_schema = LoginResponseSchema()
        access_token = create_access_token(identity=user_schema)
        token_info = decode_token(
            access_token
        )  # Accessing internal method (_decode_jwt) for token decoding
        expiration_time = token_info["exp"]
        expiration_time = datetime.fromtimestamp(expiration_time)
        login_response_schema = login_response_schema.dump(
            {"access_token": access_token, "expiration_time": expiration_time}
        )
        UserRepository.update_specific_field(user.id, "last_login_at", ts)
        return (
            jsonify(
                BaseResponseSingle(
                    login_response_schema,
                    "login successfully",
                    200,
                ).serialize()
            ),
            200,
        )
    except Exception as e:
        if "code" in e.args[0]:
            return ErrorResponse(e.args[0]["message"], e.args[0]["code"]).serialize()
        else:
            return ErrorResponse(str(e), 500).serialize()


@auth_api.route("/register", methods=["POST"])
def register():
    try:
        json = request.json
        # return jsonify(json)
        register_schema = RegisterSchema().load(json)
        user = UserRepository.get_user_by_field("nik", register_schema["nik"])
        if user:
            return ErrorResponse("nik already exist!", 400).serialize()
        user = UserRepository.get_user_by_field("email", register_schema["email"])
        if user:
            return ErrorResponse("email already exist!", 400).serialize()
        user = UserRepository.create_user(register_schema)
        if user:
            assign_role = AssignSingleRole().load(
                {"user_id": user.id, "role_name": "guest"}
            )
            user_role = UserRoleRepository.assign_single_role(assign_role)
        user_schema = UserSchema().dump(user)
        return (
            jsonify(
                BaseResponseSingle(user_schema, "created successfully", 201).serialize()
            ),
            201,
        )
    except Exception as e:
        if "code" in e.args[0]:
            return ErrorResponse(e.args[0]["message"], e.args[0]["code"]).serialize()
        else:
            return ErrorResponse(str(e), 500).serialize()


@auth_api.route("/changepassword", methods=["PATCH"])
@permission_required("Auth@changepassword")
def change_password():
    try:
        user_identity = get_jwt_identity()
        json = request.json
        schema = ChangePasswordSchema(context={"new_password": json["new_password"]})
        schema.validate(json)
        schema = schema.load(json)
        user = UserRepository.get_user_by_field("nik", user_identity["nik"])
        if user.checkPassword(schema["old_password"]) == False:
            error = ErrorSchema().load({"message": "wrong old password", "code": 400})
            raise Exception(error)
        user.setPassword(schema["new_password"])
        password = user.password
        UserRepository.update_specific_field(user.id, "password", password)
        res = BaseResponseSingle(None, "change password successfully", 200).serialize()
        return jsonify(res), 200
    except Exception as e:
        if "code" in e.args[0]:
            return ErrorResponse(e.args[0]["message"], e.args[0]["code"]).serialize()
        else:
            return ErrorResponse(str(e), 500).serialize()
