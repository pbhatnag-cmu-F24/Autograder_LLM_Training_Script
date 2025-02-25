import os
import zipfile
import json
import boto3
import PyPDF2

def unzip_repository(zip_file_path, extract_dir):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        

def extract_data_from_pdf(file_path):
    """
    Extracts text from a PDF file while handling potential PDF errors.
    
    Parameters:
        file_path (str): The path to the PDF file.
        
    Returns:
        str: The extracted text, or an empty string if extraction fails.
    """
    extracted_data = ""
    try:
        # Use strict=False to be more lenient with PDF parsing.
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f, strict=False)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    extracted_data += text
    except PyPDF2.errors.PdfReadError as e:
        print(f"Failed to extract data from {file_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while processing {file_path}: {e}")
    
    return extracted_data


def collect_repos_data(parent_dir, filenames=None):
    data_list = []
    pdf_data_list = []
    

    for repo_name in os.listdir(parent_dir):
        repo_path = os.path.join(parent_dir, repo_name)
        
        if os.path.isdir(repo_path) and not repo_name.startswith("__MACOSX"):
            repo_contents = []
            pdf_contents = []  # List to store data from PDF files
            
            for root, dirs, files in os.walk(repo_path):
                
                for file in files:

                    if file.startswith("."):
                        continue
                    
                    if file in filenames and file.endswith((".java", ".py", ".cpp")):
                        file_path = os.path.join(root, file)
                        
                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                file_data = f.read()
                                repo_contents.append(f"{file}: {file_data}")
                        except Exception as e:
                            print(f"Failed to read {file_path}: {e}")
                    
                    if file.endswith(".pdf"):
                        file_path = os.path.join(root, file)
                        
                        try:
                            extracted_data = extract_data_from_pdf(file_path)
                            pdf_contents.append(f"{file}: {extracted_data}")
                        except Exception as e:
                            print(f"Failed to extract data from {file_path}: {e}")
            
            if repo_contents:
                data_list.append("\n".join(repo_contents))
            else:
                data_list.append("")
            
            if pdf_contents:
                pdf_data_list.append("\n".join(pdf_contents))
            else:
                pdf_data_list.append("")
    
    return data_list, pdf_data_list

def pair_code_with_feedback(code_files, feedback):
    paired_data = []
    for code, fb in zip(code_files, feedback):
        paired_data.append({'code': code, 'feedback': fb})
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
zip_file_path = 'data/raw/submissions.zip'
extract_dir = 'data/raw/'
unzip_repository(zip_file_path, extract_dir)

code_directory = 'data/raw/extracted' 

# Step 2: Extract nested zip files
nested_zip_files = []
for root, dirs, files in os.walk(code_directory):
    for file in files:
        if file.endswith('.zip'):
            nested_zip_files.append(os.path.join(root, file))
            extract_dir = os.path.dirname(os.path.join(root, file))
            unzip_repository(os.path.join(root, file), extract_dir)

for zip_file_path in nested_zip_files:
    extract_dir = os.path.splitext(zip_file_path)[0]
    unzip_repository(zip_file_path, extract_dir)


# Step 3: Remove zip files
for zip_file_path in nested_zip_files:
    os.remove(zip_file_path)

# Step 4: Read code files
code_files_with_comments = collect_repos_data(code_directory, 
                                filenames=['UserService.java', 'UserOperations.java', 'CyclomaticComplexityVisitor.java',]), 

print (code_files_with_comments[0][0])
print (code_files_with_comments[0][1])

# Step 5: Pair code with feedback
#TODO: Combine datapoints with single line feedback (5/5)
paired_data = pair_code_with_feedback(code_files_with_comments[0][0], code_files_with_comments[0][1])

# def convert_to_json_array(input_dict):
#     """
#     Converts a dictionary containing 'code' and 'feedback' into a JSON array format.
    
#     :param input_dict: Dictionary with 'code' and 'feedback' pairs.
#     :return: JSON array as a string.
#     """
#     json_list = [{"code": input_dict["code"], "feedback": input_dict["feedback"]}]
#     return json.dumps(json_list, indent=4)

# json_output = convert_to_json_array(paired_data)


# Step 6: Convert to JSON
jsonl_data = convert_to_jsonl(paired_data)


# Step 7: Create dataset file
dataset_file_path = 'data/dataset.jsonl'
with open(dataset_file_path, 'w') as f:
    f.write(jsonl_data)



# Step 7: Upload to S3
# bucket_name = 'your-s3-bucket-name'
# file_name = 'dataset.jsonl'
# upload_to_s3(bucket_name, file_name, jsonl_data)

# Step 6: Fine-tune
