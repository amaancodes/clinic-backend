from flask import Blueprint, request, jsonify, current_app
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.admin.schemas import (
    DepartmentCreateRequestSchema,
    DepartmentResponseSchema,
    UserResponseSchema,
    DoctorOnboardRequestSchema,
    DoctorProfileResponseSchema,
    DoctorAssignRequestSchema,
)
from app.admin.services import AdminService
from app.core.rbac import rbac


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


class DepartmentAPI(MethodView):
    decorators = [jwt_required(), rbac("admin")]

    def post(self):
        payload = DepartmentCreateRequestSchema().load(request.get_json() or {})
        print(f"Creating department with name: {payload.get('name')}")
        current_app.logger.info(f"Creating department with name: {payload.get('name')}")
        dept = AdminService.create_department(payload["name"])
        response_data = DepartmentResponseSchema().dump(dept)
        current_app.logger.info(f"Department created: {dept.id}")
        return jsonify(response_data)

    def get(self):
        current_app.logger.info("Listing all departments")
        departments = AdminService.list_departments()
        response_data = DepartmentResponseSchema(many=True).dump(departments)
        return jsonify(response_data)


admin_bp.add_url_rule(
    "/departments", view_func=DepartmentAPI.as_view("departments")
)


class UserAPI(MethodView):
    decorators = [jwt_required(), rbac("admin")]
    def get(self):
        current_app.logger.info("Listing all users")
        users = AdminService.list_users()
        response_data = UserResponseSchema(many=True).dump(users)
        return jsonify(response_data)


admin_bp.add_url_rule("/users", view_func=UserAPI.as_view("users"))


class DoctorAPI(MethodView):
    decorators = [jwt_required(), rbac("admin")]

    def post(self):
        payload = DoctorOnboardRequestSchema().load(request.get_json() or {})
        current_app.logger.info(f"Onboarding doctor: {payload.get('email')}")
        profile = AdminService.onboard_doctor(
            payload["name"],
            payload["email"],
            payload["password"],
            payload["specialization"],
        )
        response_data = DoctorProfileResponseSchema().dump(profile)
        return jsonify(response_data), 201


admin_bp.add_url_rule("/doctors", view_func=DoctorAPI.as_view("doctors"))


class DoctorAssignmentAPI(MethodView):
    decorators = [jwt_required(), rbac("admin")]

    def post(self, doctor_id):
        payload = DoctorAssignRequestSchema().load(request.get_json() or {})
        current_app.logger.info(f"Assigning doctor {doctor_id} to department {payload['department_id']}")
        try:
            AdminService.assign_doctor(doctor_id, payload["department_id"])
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
            
        return jsonify({"message": "Doctor assigned to department successfully"}), 200


admin_bp.add_url_rule(
    "/doctors/<int:doctor_id>/assign",
    view_func=DoctorAssignmentAPI.as_view("doctor_assignment"),
)

