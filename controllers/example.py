from http import HTTPStatus
from flask import Blueprint
from flasgger import swag_from
from models.example import ExampleModel
from schemas.example import ExampleSchema

example_api = Blueprint("example_api", __name__)


@example_api.route("/")
@swag_from(
    {
        "responses": {
            HTTPStatus.OK.value: {
                "description": "Welcome to the Flask Starter Kit",
                "schema": ExampleSchema,
            }
        }
    }
)
def example():
    """

    1 liner about the route
    A more detailed description of the endpoint
    """
    result = ExampleModel()
    return ExampleSchema().dump(result), 200
