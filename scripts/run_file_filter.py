import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.services.file_filtering_service import file_name_filter, file_ext_filter

# Ensure the script can locate project modules
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Constants
FILTER_BY_EXTENSION = False  # Toggle between filename or file extension filtering

def main():
    """
    Runs the filtering service on files in SOURCE_FOLDER based on FILTER_LIST and FILTER_TYPE.
    """
    if FILTER_BY_EXTENSION:
        SOURCE_FOLDER = Path("data/unzipped")  # Folder where extracted files exist
        FILTER_TYPE = "in"  # 'in' to keep only matching files, 'out' to remove them
        FILTER_LIST = [".py", ".java", ".md"]  # Modify this for file extensions or filenames
        DEST_FOLDER = Path("data/file_filtered")  # Folder to save filtered files
        copied_files = file_ext_filter(SOURCE_FOLDER, FILTER_LIST, FILTER_TYPE, DEST_FOLDER)
        filter_type_desc = "file extension"
    else:
        SOURCE_FOLDER = Path("data/file_filtered")  # Folder where extracted files exist
        FILTER_TYPE = "out"  # 'in' to keep only matching files, 'out' to remove them
        FILTER_LIST = ['Main.java', 'DatabaseDriver.java', 'PostgresDriver.java']  # Modify this for file extensions or filenames
        copied_files = file_name_filter(SOURCE_FOLDER, FILTER_LIST, FILTER_TYPE)
        filter_type_desc = "filename"

    print(f"Filtered files based on {filter_type_desc}: {copied_files}")

if __name__ == "__main__":
    main()
