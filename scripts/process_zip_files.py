import os
import zipfile
import json
import boto3

def unzip_repository(zip_file_path, extract_dir):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

def collect_repos_data(parent_dir, max_depth=6):
    """
    Walk through each subfolder (repository) within `parent_dir`
    and collect contents of .java, .py, and .cpp files up to `max_depth` levels.

    :param parent_dir: Path to the directory that contains multiple repos.
    :param max_depth: Maximum folder depth to traverse inside each repo.
    :return: A list of strings; each string is the concatenated code of a single repo.
    """
    # This will hold one large code string per repository
    data_list = []
    
    # Helper function to check if a given path is within the desired depth
    def within_depth(current_path, base_path, max_depth):
        # relative path from the base repo directory
        rel_path = os.path.relpath(current_path, base_path)
        # count how many directories deep we are
        depth = rel_path.count(os.sep)
        return depth < max_depth

    # Iterate over the immediate subfolders in parent_dir (each subfolder is a repo)
    for repo_name in os.listdir(parent_dir):
        repo_path = os.path.join(parent_dir, repo_name)
        
        # Only process if it's actually a directory
        if os.path.isdir(repo_path):
            # Accumulate file contents for this repo
            repo_contents = []
            
            # Walk the repo directory structure
            for root, dirs, files in os.walk(repo_path):
                # If we exceed max depth, skip deeper directories
                if not within_depth(root, repo_path, max_depth):
                    # Prune subfolders to avoid going deeper
                    dirs[:] = []
                    continue
                
                # Check each file’s extension
                for file in files:
                    if file.endswith((".java", ".py", ".cpp")):
                        file_path = os.path.join(root, file)
                        
                        # Safely open and read the file contents
                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                file_data = f.read()
                                repo_contents.append(file_data)
                        except Exception as e:
                            print(f"Failed to read {file_path}: {e}")
            
            # Join all code in this repo into one string, then add to data_list
            if repo_contents:
                data_list.append("\n".join(repo_contents))
            else:
                # If you want to keep an entry for repos that have no .java/.py/.cpp files
                # you could append an empty string or skip entirely. Here we append empty:
                data_list.append("")  

    return data_list


def pair_code_with_feedback(code_files, feedback):
    paired_data = []
    for code in code_files:
        paired_data.append({'code': code, 'feedback': feedback})
    return paired_data

def convert_to_jsonl(paired_data):
    jsonl_data = ''
    for data in paired_data:
        jsonl_data += json.dumps(data) + '\n'
    return jsonl_data

def upload_to_s3(bucket_name, file_name, data):
    s3 = boto3.client('s3')
    s3.put_object(Body=data, Bucket=bucket_name, Key=file_name)

# Step 1: Unzip repository
zip_file_path = 'data/raw/task_1_submissions.zip'
extract_dir = 'data/raw/extracted'
unzip_repository(zip_file_path, extract_dir)

code_directory = 'data/raw/extracted' 
# Step 2 : Extract nested zip files
nested_zip_files = []
for root, dirs, files in os.walk(code_directory):
    for file in files:
        if file.endswith('.zip'):
            nested_zip_files.append(os.path.join(root, file))

for zip_file_path in nested_zip_files:
    extract_dir = os.path.splitext(zip_file_path)[0]
    unzip_repository(zip_file_path, extract_dir)


# Step 3: Remove zip files
for zip_file_path in nested_zip_files:
    os.remove(zip_file_path)

# Step 4: Read code files
# Replace 'data/raw/extracted' with the actual path to the extracted code directory
code_files = collect_repos_data(code_directory)

# Step 5: Pair code with feedback
feedback = 'Instructor feedback goes here'
paired_data = pair_code_with_feedback(code_files, feedback)

# Step 6: Convert to JSONL
jsonl_data = convert_to_jsonl(paired_data)

# Step 7: Upload to S3
bucket_name = 'your-s3-bucket-name'
file_name = 'dataset.jsonl'
upload_to_s3(bucket_name, file_name, jsonl_data)

# Step 6: Fine-tune
# Launch your Amazon SageMaker job with the training script, pointing to the dataset in S3