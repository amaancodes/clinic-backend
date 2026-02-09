from flask import Blueprint, request, jsonify
from flask.views import MethodView

from app.auth.services import AuthService
from app.auth.schemas import (
    RegisterRequestSchema,
    RegisterResponseSchema,
    LoginRequestSchema,
    LoginResponseSchema,
)
from app.core.exceptions import ClinicException

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


class RegisterAPI(MethodView):
    def post(self):
        try:
            payload = RegisterRequestSchema().load(request.get_json() or {})
        except ValidationError as err:
            logger.warning(f"Validation error: {err.messages}")
            raise ClinicException(str(err.messages))

        user = AuthService.register(
            payload["name"],
            payload["email"],
            payload["password"],
        payload["role"],
        )
        response_data = RegisterResponseSchema().dump(user)
        return jsonify(response_data), 201


class LoginAPI(MethodView):
    def post(self):
        payload = LoginRequestSchema().load(request.get_json() or {})
        token = AuthService.login(
            payload["email"],
            payload["password"],
        )
        response_data = LoginResponseSchema().dump({"access_token": token})
        return jsonify(response_data)


auth_bp.add_url_rule("/register", view_func=RegisterAPI.as_view("register"))
auth_bp.add_url_rule("/login", view_func=LoginAPI.as_view("login"))

