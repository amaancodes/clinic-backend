from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.appointments.schemas import (
    BookAppointmentSchema,
    AppointmentResponseSchema
)
from app.appointments.services import AppointmentService
from app.core.rbac import rbac

appointments_bp = Blueprint("appointments", __name__, url_prefix="/appointments")

@appointments_bp.route("/", methods=["POST"])
@jwt_required()
@rbac("member")
def book_appointment():
    payload = BookAppointmentSchema().load(request.get_json() or {})
    patient_id = int(get_jwt_identity())
    
    try:
        appointment = AppointmentService.book_appointment(
            patient_id=patient_id,
            doctor_id=payload["doctor_id"],
            start_time=payload["start_time"],
            end_time=payload["end_time"]
        )
        response_data = AppointmentResponseSchema().dump(appointment)
        return jsonify(response_data), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@appointments_bp.route("/", methods=["GET"])
@jwt_required()
def list_appointments():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    role = claims.get("role")
    
    appointments = AppointmentService.list_appointments(role, user_id)
    response_data = AppointmentResponseSchema(many=True).dump(appointments)
    return jsonify(response_data)
