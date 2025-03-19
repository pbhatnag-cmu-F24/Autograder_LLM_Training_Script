from flask import request

def validate_json_request(req):
    """
    Validates the incoming JSON request.
    """
    required_keys = ["extract", "map"]
    if not all(key in req for key in required_keys):
        return False, {"error": "Missing required keys in JSON"}

    return True, None
