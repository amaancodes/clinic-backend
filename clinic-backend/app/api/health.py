from flask import Blueprint, jsonify
from flask.views import MethodView

health_bp = Blueprint("health", __name__)

class HealthAPI(MethodView):
    def get(self):
        return jsonify({"status": "ok"})

health_view = HealthAPI.as_view("health")
health_bp.add_url_rule(
    "/health",
    view_func=health_view,
    methods=["GET"]
)
