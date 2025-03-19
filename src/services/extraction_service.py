import os
import json
from pathlib import Path

def extract_data_from_division(source_path, division, dest_path):
    """
    Extracts data from source_path based on the specified division and writes a JSONL dataset
    to dest_path/dataset.jsonl. Each datapoint represents a file (if division is "file")
    or a line (if division is "line").

    Params:
      source_path (str or Path): Directory with files (and subdirectories) to process.
      division (str): "file" or "line" (other divisions raise NotImplementedError).
      dest_path (str or Path): Destination folder where dataset.jsonl will be stored.

    Returns:
      str: The path to the created dataset file.
    """
    source_path = Path(source_path)
    dest_path = Path(dest_path)
    dest_path.mkdir(parents=True, exist_ok=True)
    dataset_file = dest_path / "dataset.jsonl"

    if division == "file":
        create_dataset_from_files(source_path, dataset_file)
    elif division == "line":
        create_dataset_from_lines(source_path, dataset_file)
    elif division in ("method", "class"):
        raise NotImplementedError(f"Division '{division}' is not implemented yet.")
    else:
        raise ValueError(f"Unknown division: {division}")

    return str(dataset_file)


def create_dataset_from_files(source_path, dataset_file):
    """
    Creates a JSONL dataset where each datapoint represents a file.
    Each JSON object contains:
      - "filepath": relative path of the file from source_path
      - "content": the entire content of the file

    Params:
      source_path (Path): The source directory.
      dataset_file (Path): The JSONL file to write the dataset.
    """
    with dataset_file.open("w", encoding="utf-8") as out_file:
        for root, dirs, files in os.walk(source_path):
            for file in files:
                file_path = Path(root) / file
                try:
                    with file_path.open("r", encoding="utf-8") as f:
                        content = f.read()
                    data_point = {
                        "filepath": str(file_path.relative_to(source_path)),
                        "content": content
                    }
                    out_file.write(json.dumps(data_point) + "\n")
                except Exception as e:
                    print(f"Skipping file {file_path}: {e}")


def create_dataset_from_lines(source_path, dataset_file):
    """
    Creates a JSONL dataset where each datapoint represents a non-empty line from a file.
    Each JSON object contains:
      - "filepath": relative path of the file from source_path
      - "line": a non-empty line from the file

    Params:
      source_path (Path): The source directory.
      dataset_file (Path): The JSONL file to write the dataset.
    """
    with dataset_file.open("w", encoding="utf-8") as out_file:
        for root, dirs, files in os.walk(source_path):
            for file in files:
                file_path = Path(root) / file
                try:
                    with file_path.open("r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line:  # Only write non-empty lines
                                data_point = {
                                    "filepath": str(file_path.relative_to(source_path)),
                                    "line": line
                                }
                                out_file.write(json.dumps(data_point) + "\n")
                except Exception as e:
                    print(f"Skipping file {file_path}: {e}")
