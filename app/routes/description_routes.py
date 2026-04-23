from flask import Blueprint, jsonify, request
from app.services.description_service import (
    create_description,
    delete_description_by_id,
    get_all_descriptions,
)


description_bp = Blueprint("description", __name__)
ALLOWED_TONES = {"formal", "santai", "persuasif"}


@description_bp.route("/descriptions/generate", methods=["POST"])
def generate_description():
    data = request.get_json(silent=True) or {}

    product_name = str(data.get("product_name") or "").strip()
    platform = str(data.get("platform") or "").strip()
    tone = str(data.get("tone") or "").strip().lower()

    features_raw = data.get("features")
    if isinstance(features_raw, list):
        features = [str(item).strip() for item in features_raw if str(item).strip()]
    else:
        features = []

    if not product_name:
        return jsonify({"error": "product_name is required"}), 400
    if not features:
        return jsonify({"error": "features must be a non-empty list"}), 400
    if not platform:
        return jsonify({"error": "platform is required"}), 400
    if tone not in ALLOWED_TONES:
        return jsonify({"error": "tone must be one of: formal, santai, persuasif"}), 400

    try:
        result = create_description(product_name, features, platform, tone)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@description_bp.route("/descriptions", methods=["GET"])
def get_descriptions():
    data = get_all_descriptions()
    return jsonify(data)


@description_bp.route("/descriptions/<int:description_id>", methods=["DELETE"])
def delete_description(description_id: int):
    try:
        deleted = delete_description_by_id(description_id)
        if not deleted:
            return jsonify({"error": "Description not found"}), 404
        return jsonify({"message": "Description deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
