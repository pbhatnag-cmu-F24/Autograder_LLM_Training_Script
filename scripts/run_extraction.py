import argparse
import json
from pathlib import Path
from src.services.extraction_service import process_extraction

def main():
    parser = argparse.ArgumentParser(description="Run Extraction Service to unzip code files.")
    parser.add_argument(
        "--zip-files", 
        nargs="+", 
        required=True, 
        help="List of zip file paths to extract (e.g., --zip-files uploads/code.zip)"
    )
    args = parser.parse_args()

    # Build the extraction request
    extraction_request = {
        "filter_out": [],  # add filters as needed
        "file": [str(Path(z).resolve()) for z in args.zip_files],
        "division": {
            "file": True,
            "method": True,
            "class": True,
            "line": True
        },
        "filters": {
            "file_extension": {"include": [".py"], "exclude": []},
            "filename": {"include": ["csv"], "exclude": []},
            "method_name": {"include": ["csv"], "exclude": []},
            "class_name": {"include": [], "exclude": []}
        }
    }

    # Process extraction using the service
    result = process_extraction(extraction_request)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
