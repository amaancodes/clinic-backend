from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.doctors.schemas import (
    DoctorOnboardRequestSchema,
    DoctorProfileResponseSchema,
    DoctorAssignRequestSchema,
    DoctorAvailabilityRequestSchema,
    AvailabilitySchema
)
from app.doctors.services import DoctorService
from app.core.rbac import rbac

doctors_bp = Blueprint("doctors", __name__, url_prefix="/doctors")

@doctors_bp.route("/", methods=["POST"])
@jwt_required()
@rbac("admin")
def onboard_doctor():
    payload = DoctorOnboardRequestSchema().load(request.get_json() or {})
    try:
        doctor = DoctorService.onboard_doctor(
            name=payload["name"],
            email=payload["email"],
            password=payload["password"],
            specialization=payload["specialization"]
        )
        response_data = DoctorProfileResponseSchema().dump(doctor)
        return jsonify(response_data), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@doctors_bp.route("/<int:doctor_id>/assign", methods=["PUT"])
@jwt_required()
@rbac("admin")
def assign_doctor(doctor_id):
    payload = DoctorAssignRequestSchema().load(request.get_json() or {})
    try:
        DoctorService.assign_department(doctor_id, payload["department_id"])
        return jsonify({"message": "Doctor assigned to department successfully"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@doctors_bp.route("/availability", methods=["POST"])
@jwt_required()
@rbac("doctor")
def manage_availability():
    payload = DoctorAvailabilityRequestSchema().load(request.get_json() or {})
    current_user_id = int(get_jwt_identity())
    try:
        DoctorService.set_availability(current_user_id, payload["availabilities"])
        return jsonify({"message": "Availability updated successfully"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@doctors_bp.route("/list", methods=["GET"])
@jwt_required()
def list_doctors():
    doctors = DoctorService.list_doctors()
    response_data = DoctorProfileResponseSchema(many=True).dump(doctors)
    return jsonify(response_data)

@doctors_bp.route("/<int:doctor_id>/availability", methods=["GET"])
@jwt_required()
def get_availability(doctor_id):
    availabilities = DoctorService.get_doctor_availability(doctor_id)
    response_data = AvailabilitySchema(many=True).dump(availabilities)
    return jsonify(response_data)
