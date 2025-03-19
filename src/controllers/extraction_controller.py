import sys
from pathlib import Path
from flask import Blueprint, request, jsonify, send_file

# Ensure the project root is in sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.services.extraction_service import extract_data_from_division

# Hardcoded folders
SOURCE_FOLDER = "data/file_filtered"
DEST_FOLDER = "data/divisioned"
DATASET_FILENAME = "dataset.jsonl"

# Create a blueprint for dataset extraction endpoints
dataset_extraction_bp = Blueprint("dataset_extraction_bp", __name__)

@dataset_extraction_bp.route("/api/dataset/extraction", methods=["POST"])
def dataset_extraction_controller():
    """
    Creates a dataset by processing files from SOURCE_FOLDER.
    The request JSON should include a "division" parameter (one of: "file", "line", "method", or "class").
    The dataset is stored in DEST_FOLDER and returned as a downloadable file.
    """
    req_data = request.get_json()
    if not req_data:
        return jsonify({"error": "Missing JSON request body"}), 400

    division = req_data.get("division")
    if not division:
        return jsonify({"error": "Missing 'division' parameter in request"}), 400

    try:
        dataset_file_path = extract_data_from_division(SOURCE_FOLDER, division, DEST_FOLDER)
        dataset_file = Path(dataset_file_path)

        if not dataset_file.exists():
            return jsonify({"error": "Dataset file not found"}), 500

        # Return the file as a downloadable response
        return send_file(dataset_file, as_attachment=True, mimetype="application/jsonl")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
