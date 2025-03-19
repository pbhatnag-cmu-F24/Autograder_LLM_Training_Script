from flask import Blueprint, request, jsonify
from services.extraction_service import process_extraction
from schemas.extraction_schemas import validate_json_request

extraction_bp = Blueprint("extraction", __name__)

@extraction_bp.route("/extract", methods=["POST"])
def extract_code():
    """
    Handles the extraction request.
    """
    req_data = request.get_json()

    # Validate request
    is_valid, error_response = validate_json_request(req_data)
    if not is_valid:
        return jsonify(error_response), 400

    extract_data = req_data["extract"]
    response_data = process_extraction(extract_data)

    return jsonify({"message": "Extraction successful", "data": response_data}), 200
