from flask.views import MethodView
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.core.rbac import role_required
from app.services.admin_service import AdminService

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

class DepartmentAPI(MethodView):

    decorators = [jwt_required(), role_required("admin")]

    def post(self):
        dept = AdminService.create_department(request.json["name"])
        return jsonify({"id": dept.id})

    def get(self):
        from app.models.department import Department
        return jsonify([
            {"id": d.id, "name": d.name} for d in Department.query.all()
        ])
