from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required

from app.departments.schemas import (
    DepartmentCreateRequestSchema,
    DepartmentResponseSchema,
)
from app.departments.services import DepartmentService
from app.core.rbac import rbac

departments_bp = Blueprint("departments", __name__, url_prefix="/departments")

@departments_bp.route("/", methods=["POST"])
@jwt_required()
@rbac("admin")
def create_department():
    try:
        payload = DepartmentCreateRequestSchema().load(request.get_json() or {})
        current_app.logger.info(f"Creating department with name: {payload.get('name')}")
        dept = DepartmentService.create_department(payload["name"])
        response_data = DepartmentResponseSchema().dump(dept)
        current_app.logger.info(f"Department created: {dept.id}")
        return jsonify(response_data), 201
    except Exception as e:
        current_app.logger.error(f"Error creating department: {str(e)}")
        return jsonify({"message": str(e)}), 400

@departments_bp.route("/", methods=["GET"])
@jwt_required()
@rbac("admin")
def list_departments():
    try:
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)

        current_app.logger.info("Listing all departments")
        departments = DepartmentService.list_departments(limit=limit, offset=offset)
        response_data = DepartmentResponseSchema(many=True).dump(departments)
        return jsonify(response_data), 200
    except Exception as e:
        current_app.logger.error(f"Error listing departments: {str(e)}")
        return jsonify({"message": str(e)}), 400 