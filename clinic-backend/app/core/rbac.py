from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import abort

def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if identity["role"] not in allowed_roles:
                abort(403, "Forbidden")
            return fn(*args, **kwargs)
        return wrapper
    return decorator
