import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.services.dataset_processing_service import process_dataset

# Add project root to sys.path so that imports work correctly
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Constants
INPUT_FILE = "data/divisioned/unprocessed_dataset.jsonl"  # Path to the unprocessed dataset (JSONL)
DATASET_DIVISION = "method"  # Options: "file", "method", or "class"
FILTER = ("out", ['getId', 'setId', 'getUsername', 'setUsername', 'getAge', 'setAge', 'toString'])  # Tuple: (filter_type, list of filters)
DESTINATION_FOLDER = "data/processed"  # Folder to store the processed dataset

def main():
    processed_dataset_path = process_dataset(INPUT_FILE, DATASET_DIVISION, FILTER, DESTINATION_FOLDER)
    result = {
        "message": "Processed dataset created successfully.",
        "processed_dataset_path": processed_dataset_path
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
