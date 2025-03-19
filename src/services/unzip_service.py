import os
import zipfile
from pathlib import Path

def recursive_unzip(zip_files, destination):
    """
    Recursively unzips all zip files in the given list and any zip files found within extracted folders.

    Args:
        zip_files (list): A list of paths (str or Path) to zip files to extract.
        destination (str or Path): The root destination directory for extraction.

    Returns:
        list: A list of all extracted file paths (as strings).
    """
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    extracted_files = []

    # Process each zip file in the list
    for zip_file in zip_files:
        zip_path = Path(zip_file)
        # Get the current filename
        filename = zip_path.name
        # Remove the suffix after '.'
        filename = filename.split('.')[0]

        # Append the current filename to the destination
        destination_with_filename = destination / filename

        # Create the destination directory for the current zip file
        destination_with_filename.mkdir(parents=True, exist_ok=True)

        # Update the destination to the new directory
        if not zip_path.is_file() or zip_path.suffix.lower() != ".zip":
            continue

        # Extract the current zip file
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                # Extract all files in the current zip file
                for member in zf.infolist():
                    # Check if the member is a directory
                    if member.is_dir():
                        continue

                    # Extract the member to the destination directory while maintaining the folder structure
                    zf.extract(member, destination_with_filename)
                    extracted_files.append(str(destination_with_filename / member.filename))
        except Exception as e:
            print(f"Error extracting {zip_path}: {e}")
            continue

        # Delete all the .zip files in current folder
        # for file in os.listdir(destination_with_filename):
        #     if file.endswith(".zip"):
        #         os.remove(destination_with_filename / file)
        # Check extracted files for nested zip files
        nested_zip_files = [str(destination_with_filename / member.filename) for member in zf.infolist() if member.filename.endswith(".zip")]
        if nested_zip_files:
            # Recursively unzip any nested zip files 
            nested_extracted = recursive_unzip(nested_zip_files, destination_with_filename)
            extracted_files.extend(nested_extracted)

    return extracted_files

# # Example usage as a script:
# if __name__ == "__main__":
#     import argparse
#     import json

#     parser = argparse.ArgumentParser(
#         description="Recursively unzip all provided zip files into a destination directory."
#     )
#     parser.add_argument(
#         "--zip-files", nargs="+", required=True,
#         help="Paths to one or more zip files to extract."
#     )
#     parser.add_argument(
#         "--destination", default="data/extracted",
#         help="Destination directory for extraction (default: data/extracted)"
#     )
#     args = parser.parse_args()

#     # Run recursive unzip
#     results = recursive_unzip(args.zip_files, args.destination)
#     print(json.dumps({"extracted_files": results}, indent=2))
