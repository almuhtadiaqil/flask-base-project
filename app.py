from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from argparse import ArgumentParser
from flask_cors import CORS
from flasgger import Swagger
import logging
from common.base_response import BaseResponse
from flask_jwt_extended import JWTManager, jwt_required
from sentry_sdk.integrations.flask import FlaskIntegration
from config import Config
from schemas.error_schema import ErrorSchema
from common.error_response import ErrorResponse
from common.base_response_single import BaseResponseSingle
from flask.cli import FlaskGroup


db = SQLAlchemy()
app = Flask(__name__)
# app.config["JSON_SORT_KEYS"] = False
app.config.from_object(os.environ["APP_SETTINGS"])
# app.config.from_object(os.environ{})

jwt = JWTManager(app)
CORS(app)
db.init_app(app)
migrate = Migrate(app=app, db=db)
Swagger(app)


# @jwt.expired_token_loader
# def my_expired_token_callback(jwt_header, jwt_payload):
#     response = BaseResponse(None, "Token Expired", 0, 0, 0, 401)
#     return jsonify(response.serialize()), 401


def method_not_allowed_exception(e):
    response = BaseResponse(None, "Method not Allowed", 0, 0, 0, 401)
    return jsonify(response.serialize()), 405


def notfound_exception(e):
    response = BaseResponse(None, "Endpoint Not Found", 0, 0, 0, 401)
    return jsonify(response.serialize()), 404


@app.errorhandler(Exception)
def handle_exception(e):
    if "code" in e.args[0]:
        return ErrorResponse(e.args[0]["message"], e.args[0]["code"]).serialize()
    else:
        return ErrorResponse(exception=str(e), code=500).serialize()


app.register_error_handler(404, notfound_exception)
app.register_error_handler(405, method_not_allowed_exception)


@app.route("/api/v1/debug-sentry")
def trigger_error():
    division_by_zero = 1 / 0


from controllers.user_controller import user_api
from controllers.auth_controller import auth_api
from controllers.role_controller import role_api
from controllers.permission_controller import permission_api

path_api = "/api/v1"
app.register_blueprint(user_api, url_prefix=path_api)
app.register_blueprint(auth_api, url_prefix=path_api)
app.register_blueprint(role_api, url_prefix=path_api + "/roles")
app.register_blueprint(permission_api, url_prefix=path_api + "/permissions")

from command.permission_command import permission_commands

app.cli.add_command(permission_commands)


if __name__ == "__main__":
    # app = create_app()
    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5000, type=int, help="Port to listen on"
    )
    args = parser.parse_args()
    port = args.port
    app.run()
