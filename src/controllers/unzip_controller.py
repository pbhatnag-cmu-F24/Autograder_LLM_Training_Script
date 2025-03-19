import os
import shutil
from pathlib import Path
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from src.services.unzip_service import recursive_unzip

RAW_DATA_DIR = Path("data/raw")
UNZIPPED_DATA_DIR = Path("data/unzipped")

unzip_bp = Blueprint("unzip_bp", __name__)

def clear_directory(directory: Path):
    """Removes all content in the directory and recreates it."""
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)

@unzip_bp.route("/unzip", methods=["POST"])
def unzip_controller():
    """
    Receives a zip file via a JSON multipart/form-data request.
    It clears RAW_DATA_DIR, saves the uploaded file into RAW_DATA_DIR, 
    then recursively unzips all zip files from RAW_DATA_DIR into UNZIPPED_DATA_DIR.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not RAW_DATA_DIR.exists():
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    clear_directory(RAW_DATA_DIR)

    if not UNZIPPED_DATA_DIR.exists():
        UNZIPPED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    clear_directory(UNZIPPED_DATA_DIR)

    filename = secure_filename(uploaded_file.filename)
    save_path = RAW_DATA_DIR / filename
    uploaded_file.save(str(save_path))

    zip_files = list(RAW_DATA_DIR.glob("*.zip"))
    if not zip_files:
        return jsonify({"error": "No zip files found in RAW_DATA_DIR"}), 400

    unzipped_files = recursive_unzip(zip_files, UNZIPPED_DATA_DIR)

    return jsonify({
        "message": "Unzipping completed successfully.",
        "unzipped_files": unzipped_files
    }), 200
