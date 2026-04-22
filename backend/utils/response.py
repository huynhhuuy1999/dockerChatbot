from flask import jsonify
from utils.constants import STATUS


def response_success(**data):
    payload = {"status": "success", **data}
    return jsonify(payload)


def response_error(error, status_code=STATUS["BAD_REQUEST"], **data):
    payload = {"status": "error", **data}
    if error:
        payload["error"] = error

    return jsonify(payload), status_code
