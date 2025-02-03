import os
import zipfile
import json
import boto3

def unzip_repository(zip_file_path, extract_dir):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

def read_code_files(directory):
    code_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code = f.read()
                    code_files.append(code)
    return code_files

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
zip_file_path = 'path/to/zip/file.zip'
extract_dir = 'path/to/extract/directory'
unzip_repository(zip_file_path, extract_dir)

# Step 2: Read code files
code_directory = 'path/to/code/directory'
code_files = read_code_files(code_directory)

# Step 3: Pair code with feedback
feedback = 'Instructor feedback goes here'
paired_data = pair_code_with_feedback(code_files, feedback)

# Step 4: Convert to JSONL
jsonl_data = convert_to_jsonl(paired_data)

# Step 5: Upload to S3
bucket_name = 'your-s3-bucket-name'
file_name = 'dataset.jsonl'
upload_to_s3(bucket_name, file_name, jsonl_data)

# Step 6: Fine-tune
# Launch your Amazon SageMaker job with the training script, pointing to the dataset in S3