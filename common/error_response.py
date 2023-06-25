from common.base_response_single import BaseResponseSingle
from flask import jsonify


class ErrorResponse(object):
    data = None
    status = False
    message = None
    total = 0
    page = 0
    limit = 0
    code = 500

    def __init__(self, exception, code):
        self.message = str(exception) if exception is not None else None
        self.code = code

    def serialize(self):
        return (
            jsonify(BaseResponseSingle(None, self.code, self.message).serialize()),
            self.code,
        )
