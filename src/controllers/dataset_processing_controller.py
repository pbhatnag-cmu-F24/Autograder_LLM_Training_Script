import sys
from pathlib import Path
from flask import Blueprint, request, jsonify, send_file

# Ensure the project root is in sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.services.dataset_processing_service import process_dataset

# Hardcoded Constants
INPUT_FILE = "data/divisioned/unprocessed_dataset.jsonl"  # Path to the unprocessed dataset
DESTINATION_FOLDER = "data/processed"  # Folder where the processed dataset will be stored

# Create a blueprint for dataset processing
dataset_processing_bp = Blueprint("dataset_processing_bp", __name__)

@dataset_processing_bp.route("/api/dataset/process", methods=["POST"])
def dataset_processing_controller():
    """
    Processes the dataset by applying filters.
    The request JSON should contain:
      - "dataset_division": One of "file", "method", or "class".
      - "filter_type": Either "in" (keep only matching records) or "out" (remove matching records).
      - "filter_list": A list of strings to match against filenames, method names, or class names.
    
    Returns the processed dataset as a downloadable file.
    """
    req_data = request.get_json()
    if not req_data:
        return jsonify({"error": "Missing JSON request body"}), 400

    dataset_division = req_data.get("dataset_division")
    filter_type = req_data.get("filter_type")
    filter_list = req_data.get("filter_list")

    if not dataset_division or dataset_division not in ["file", "method", "class"]:
        return jsonify({"error": "Invalid or missing 'dataset_division' parameter"}), 400
    if filter_type not in ["in", "out"]:
        return jsonify({"error": "Invalid filter type, must be 'in' or 'out'"}), 400
    if not isinstance(filter_list, list):
        return jsonify({"error": "'filter_list' must be a list of strings"}), 400

    try:
        processed_dataset_path = process_dataset(
            INPUT_FILE, dataset_division, (filter_type, filter_list), DESTINATION_FOLDER
        )
        processed_file = Path(processed_dataset_path)

        if not processed_file.exists():
            return jsonify({"error": "Processed dataset file not found"}), 500

        # Return the processed file as a downloadable response
        return send_file(processed_file, as_attachment=True, mimetype="application/jsonl")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
