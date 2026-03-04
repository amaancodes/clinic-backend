from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask import abort

def rbac(role: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if not claims or claims.get("role") != role:
                abort(403, "Forbidden")
            return fn(*args, **kwargs)
        return wrapper
    return decorator
