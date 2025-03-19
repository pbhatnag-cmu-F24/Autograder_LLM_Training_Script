import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))


from src.services.extraction_service import extract_data_from_division

# Add the project root to sys.path so that imports work correctly
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Constants for running the service
SOURCE_FOLDER = "data/file_filtered"         # Folder containing the raw files to process
DEST_FOLDER = "data/divisioned"     # Folder where dataset.jsonl will be stored
DIVISION = "method"                  # "file" or "line" or "class" or "method"

def main():
    # Create the dataset by extracting data based on the chosen division
    dataset_file_path = extract_data_from_division(SOURCE_FOLDER, DIVISION, DEST_FOLDER)
    
    # Print the output in JSON format
    result = {
        "message": "Dataset created successfully.",
        "dataset_path": dataset_file_path
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
