from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.admin.schemas import (
    DepartmentCreateRequestSchema,
    DepartmentResponseSchema,
)
from app.admin.services import AdminService
from app.core.rbac import role_required


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


class DepartmentAPI(MethodView):
    decorators = [jwt_required(), role_required("admin")]

    def post(self):
        payload = DepartmentCreateRequestSchema().load(request.get_json() or {})
        dept = AdminService.create_department(payload["name"])
        response_data = DepartmentResponseSchema().dump(dept)
        return jsonify(response_data)

    def get(self):
        departments = AdminService.list_departments()
        response_data = DepartmentResponseSchema(many=True).dump(departments)
        return jsonify(response_data)


admin_bp.add_url_rule(
    "/departments", view_func=DepartmentAPI.as_view("departments")
)

