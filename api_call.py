import json
import requests


def run_api():
        # URL for the extract endpoint
    url = "http://localhost:8080/extract"
    

    # Open the zip file in binary mode
    with open("data/raw/task_1_submissions.zip", "rb") as zip_file:
        # Prepare the filter configuration as a JSON string
        filter_config = json.dumps({
            "filter_out": ["ignore.py"],
            "division": {"file": True, "method": True, "class": False, "line": False},
            "file_extension_filter": [".py"],
            "file_extension_filter_type": "in",
            "filename_filter_in": ["example"],
            "filename_filter_type": "in",
            "methodname_filter": ["init"],
            "methodname_filter_type": "in",
            "classname_filter": ["Test"],
            "classname_filter_type": "in"
        })

        # Build the request with file and form-data
        print(filter_config)
        response = requests.post(url, 
                                files={"file": zip_file},
                                data={"filter_config": filter_config})
        
        # Print out the JSON response
        print(response.json())


if __name__ == "__main__":
    run_api()