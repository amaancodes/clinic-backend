from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.reimbursements import reimbursements_bp
from app.reimbursements.services import ReimbursementService
from app.reimbursements.schemas import ReimbursementCreateSchema, ReimbursementResponseSchema, ReimbursementUpdateSchema
from app.core.feature_flags import require_feature
from app.core.rbac import rbac
from app.core.enum import Role, ReimbursementStatus

reimbursement_schema = ReimbursementCreateSchema()
reimbursement_response_schema = ReimbursementResponseSchema()
reimbursements_schema = ReimbursementResponseSchema(many=True)
reimbursement_update_schema = ReimbursementUpdateSchema()

@reimbursements_bp.route("/reimbursements", methods=["POST"])
@jwt_required()
@rbac(Role.member)
@require_feature("reimbursement_module")
def create_reimbursement():
    data = request.get_json()
    errors = reimbursement_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    current_user_id = get_jwt_identity()
    reimbursement = ReimbursementService.create_reimbursement(data, current_user_id)
    return jsonify(reimbursement_response_schema.dump(reimbursement)), 201

@reimbursements_bp.route("/reimbursements", methods=["GET"])
@jwt_required()
@require_feature("reimbursement_module")
def get_reimbursements():
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role")
    
    reimbursements = ReimbursementService.get_reimbursements(current_user_id, role)
    return jsonify(reimbursements_schema.dump(reimbursements)), 200

@reimbursements_bp.route("/reimbursements/<int:id>/status", methods=["PUT"])
@jwt_required()
@rbac(Role.admin)
@require_feature("reimbursement_module")
def update_reimbursement_status(id):
    data = request.get_json()
    errors = reimbursement_update_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    status = data.get("status")
    reimbursement = ReimbursementService.update_reimbursement_status(id, status)
    return jsonify(reimbursement_response_schema.dump(reimbursement)), 200
