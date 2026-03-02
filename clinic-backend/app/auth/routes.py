from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import logging
from app.auth.services import AuthService
from app.core.exceptions import ClinicException, AuthenticationError
from marshmallow import ValidationError
from app.auth.schemas import RegisterSchema, LoginSchema, RoleAssignmentSchema
from app.auth.models import User
from app.core.extensions import db
from app.core.rbac import rbac

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        payload = RegisterSchema().load(request.get_json() or {})
    except ValidationError as err:
        current_app.logger.warning(f"Validation error: {err.messages}")
        raise ClinicException(str(err.messages))

    except Exception as e:
        current_app.logger.error(f"Error registering user: {str(e)}")
        return jsonify({"message": str(e)}), 400

    try:
        user = AuthService.register(
            payload["name"],
            payload["email"],
            payload["password"],
        )
        response_data = {"message": "User registered", "user_id": user.id}
        return jsonify(response_data), 201
    except Exception as e:
        current_app.logger.error(f"Error processing registration: {str(e)}")
        return jsonify({"message": str(e)}), 400

@auth_bp.route("/login", methods=["POST"])
def login():
    payload = LoginSchema().load(request.get_json() or {})
    try:
        result = AuthService.login(
            payload["email"],
            payload["password"],
        )
        current_app.logger.info(f"User logged in: {result['user_id']}")
        response_data = {
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"]
        }
        return jsonify(response_data), 200
    except AuthenticationError as e:
        return jsonify({"message": str(e)}), 401
    except Exception as e:
        current_app.logger.error(f"Error logging in: {str(e)}")
        return jsonify({"message": str(e)}), 400

from app.core.constants import ErrorMessages

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user_id = get_jwt_identity()
        # We might want to re-fetch the user to get current role if we put role in access token
        user = db.session.get(User, int(current_user_id))
        if not user:
            return jsonify({"message": ErrorMessages.USER_NOT_FOUND}), 404
            
        new_access_token = create_access_token(
            identity=current_user_id,
            additional_claims={"role": str(user.role.value)}
        )
        return jsonify(access_token=new_access_token), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@auth_bp.route("/users/<int:user_id>/role", methods=["PUT"])
@jwt_required()
@rbac("admin")
def assign_role(user_id):
    try:
        payload = RoleAssignmentSchema().load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"message": str(err.messages)}), 400

    try:
        user = AuthService.assign_role(user_id, payload["role"])
        return jsonify({"message": f"Role updated to {user.role.value}", "user_id": user.id}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

