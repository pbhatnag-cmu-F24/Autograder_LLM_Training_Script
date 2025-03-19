import sys
from pathlib import Path
import json

# Ensure the script can locate project modules
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.services.unzip_service import recursive_unzip

# Define paths
RAW_DATA_DIR = Path("data/raw")
UNZIPPED_DATA_DIR = Path("data/unzipped")

def main():
    """
    Finds all zip files in data/raw and extracts them recursively into data/extracted.
    """
    # Ensure the directories exist
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    UNZIPPED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Collect all zip files in data/raw
    zip_files = list(RAW_DATA_DIR.glob("*.zip"))

    if not zip_files:
        print("No zip files found in data/raw.")
        return

    # Perform recursive extraction
    unzipped_files = recursive_unzip(zip_files, UNZIPPED_DATA_DIR)

    # Print the results in JSON format
    result = {"unzipped_files": unzipped_files}
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
