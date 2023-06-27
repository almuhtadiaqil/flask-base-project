from flask import Blueprint, request, jsonify
from models.user_model import User
from schemas.user_schema import UserSchema
from schemas.pagination_schema import PaginationSchema
from schemas.error_schema import ErrorSchema
from common.base_response import BaseResponse
from common.base_response_single import BaseResponseSingle
from common.error_response import ErrorResponse
from repositories.user_repository import UserRepository
from flask_jwt_extended import *
from schemas.auth_schema import LoginSchema, RegisterSchema

auth_api = Blueprint("auth_api", __name__)

@auth_api.route("/login",methods=["POST"])
def login():
    request_data = LoginSchema()
    json = request.json
    request_data = request_data.load(json)
    try:
        user = UserRepository.get_user_by_field("nik",request_data.nik)
        if user is None
    except print(0):
        pass