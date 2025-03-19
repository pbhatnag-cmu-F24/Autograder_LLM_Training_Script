import json
from pathlib import Path

def process_dataset(input_filepath, dataset_division, filter_tuple, destination_folder):
    """
    Processes an unprocessed dataset JSONL file and filters the data based on the dataset_division and filter.
    
    Args:
        input_filepath (str or Path): Path to the unprocessed dataset file (JSONL format).
        dataset_division (str): One of "file", "method", or "class".
        filter_tuple (tuple): Tuple of (filter_type, filters), where filter_type is either 'in' or 'out'
                              and filters is a list of strings for matching.
        destination_folder (str or Path): Folder where the processed dataset will be stored.
    
    Returns:
        str: The path to the processed dataset file.
    """
    filter_type, filters = filter_tuple
    if filter_type not in ['in', 'out']:
        raise ValueError("filter_type must be either 'in' or 'out'.")

    input_filepath = Path(input_filepath)
    destination_folder = Path(destination_folder)
    destination_folder.mkdir(parents=True, exist_ok=True)
    output_filepath = destination_folder / "processed_dataset.jsonl"

    with input_filepath.open("r", encoding="utf-8") as infile, output_filepath.open("w", encoding="utf-8") as outfile:
        for line in infile:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            keep = False

            if dataset_division == "file":
                # Expected record format: {"filepath": ..., "filename": ..., "content": ...}
                filename = record.get("filename", "")
                if filter_type == "in":
                    if filename in filters:
                        keep = True
                else:  # filter_type == "out"
                    if filename not in filters:
                        keep = True

            elif dataset_division == "method":
                # Expected record format: {"filepath": ..., "method": {"name": ..., "content": ...}}
                method = record.get("method", {})
                method_name = method.get("name", "")
                if filter_type == "in":
                    if method_name in filters:
                        keep = True
                else:  # filter_type == "out"
                    if method_name not in filters:
                        keep = True

            elif dataset_division == "class":
                # Expected record format: {"filepath": ..., "class": {"name": ..., "content": ...}}
                cls = record.get("class", {})
                class_name = cls.get("name", "")
                if filter_type == "in":
                    if class_name in filters:
                        keep = True
                else:  # filter_type == "out"
                    if class_name not in filters:
                        keep = True
            else:
                raise ValueError("dataset_division must be one of 'file', 'method', or 'class'.")

            if keep:
                outfile.write(json.dumps(record) + "\n")

    return str(output_filepath)
