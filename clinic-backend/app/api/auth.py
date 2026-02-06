from flask import Blueprint, request, jsonify
from flask.views import MethodView
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

class RegisterAPI(MethodView):
    def post(self):
        data = request.json
        user = AuthService.register(
            data["email"], data["password"], data["role"]
        )
        return jsonify({"id": user.id}), 201

class LoginAPI(MethodView):
    def post(self):
        token = AuthService.login(
            request.json["email"],
            request.json["password"]
        )
        return jsonify({"access_token": token})

auth_bp.add_url_rule("/register", view_func=RegisterAPI.as_view("register"))
auth_bp.add_url_rule("/login", view_func=LoginAPI.as_view("login"))
