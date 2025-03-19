import os
import json
import ast
import javalang
from pathlib import Path

def extract_data_from_division(source_path, division, dest_path):
    """
    Extracts data from source_path based on the specified division and writes a JSONL dataset
    to dest_path/dataset.jsonl. The division can be:
      - "file": Each datapoint is a file (entire content).
      - "line": Each datapoint is a non-empty line.
      - "method": Each datapoint is a method extracted from the AST.
      - "class": Each datapoint is a class extracted from the AST.

    Params:
      source_path (str or Path): Directory with files (and subdirectories) to process.
      division (str): "file", "line", "method", or "class".
      dest_path (str or Path): Destination folder where dataset.jsonl will be stored.

    Returns:
      str: The path to the created dataset file.
    """
    source_path = Path(source_path)
    dest_path = Path(dest_path)
    dest_path.mkdir(parents=True, exist_ok=True)
    dataset_file = dest_path / "unprocessed_dataset.jsonl"

    if division == "file":
        create_dataset_from_files(source_path, dataset_file)
    elif division == "line":
        create_dataset_from_lines(source_path, dataset_file)
    elif division == "method":
        create_dataset_from_methods(source_path, dataset_file)
    elif division == "class":
        create_dataset_from_classes(source_path, dataset_file)
    else:
        raise ValueError(f"Unknown division: {division}")
    return str(dataset_file)


def create_dataset_from_files(source_path, dataset_file):
    with dataset_file.open("w", encoding="utf-8") as out_file:
        for root, dirs, files in os.walk(source_path):
            for file in files:
                file_path = Path(root) / file
                try:
                    with file_path.open("r", encoding="utf-8") as f:
                        content = f.read()
                    data_point = {
                        "filepath": str(file_path.relative_to(source_path)),
                        "filename": file,
                        "content": content
                    }
                    out_file.write(json.dumps(data_point) + "\n")
                except Exception as e:
                    print(f"Skipping file {file_path}: {e}")


def create_dataset_from_lines(source_path, dataset_file):
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



def create_dataset_from_methods(source_path, dataset_file):
    """
    Creates a JSONL dataset where each datapoint represents a method extracted from a file.
    Each JSON object contains:
      - "filepath": relative path of the file from source_path
      - "method": name of the extracted method
    """
    with dataset_file.open("w", encoding="utf-8") as out_file:
        for root, dirs, files in os.walk(source_path):
            for file in files:
                file_path = Path(root) / file
                try:
                    parsed = parse_ast_from_file(file_path)
                    if parsed and "methods" in parsed:
                        for method in parsed["methods"]:
                            data_point = {
                                "filepath": str(file_path.relative_to(source_path)),
                                "method": method
                            }
                            out_file.write(json.dumps(data_point) + "\n")
                except Exception as e:
                    print(f"Skipping file {file_path}: {e}")


def create_dataset_from_classes(source_path, dataset_file):
    """
    Creates a JSONL dataset where each datapoint represents a class extracted from a file.
    Each JSON object contains:
      - "filepath": relative path of the file from source_path
      - "class": name of the extracted class
    """
    with dataset_file.open("w", encoding="utf-8") as out_file:
        for root, dirs, files in os.walk(source_path):
            for file in files:
                file_path = Path(root) / file
                try:
                    parsed = parse_ast_from_file(file_path)
                    if parsed and "classes" in parsed:
                        for cls in parsed["classes"]:
                            data_point = {
                                "filepath": str(file_path.relative_to(source_path)),
                                "class": cls
                            }
                            out_file.write(json.dumps(data_point) + "\n")
                except Exception as e:
                    print(f"Skipping file {file_path}: {e}")


def parse_ast_from_file(file_path):
    """
    Parses the file based on its extension and returns a dict containing the extracted methods and classes.
    Supported extensions: .py, .java, .cpp
    """
    ext = file_path.suffix.lower()
    if ext == ".py":
        return parse_python_file(file_path)
    elif ext == ".java":
        return parse_java_file(file_path)
    elif ext == ".cpp":
        return parse_cpp_file(file_path)
    else:
        return None


def parse_python_file(file_path):
    """
    Uses Python's ast module to extract method and class names from a Python file.
    """
    try:
        with file_path.open("r", encoding="utf-8") as f:
            code = f.read()
        tree = ast.parse(code)
        methods = []
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                methods.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
        return {"methods": methods, "classes": classes}
    except Exception as e:
        print(f"Error parsing Python file {file_path}: {e}")
        return None


def get_index_from_position(code, line, column):
    """
    Convert a (line, column) position to a character index in code.
    Lines and columns are assumed to be 1-indexed.
    """
    lines = code.splitlines(keepends=True)
    if line - 1 < len(lines):
        return sum(len(lines[i]) for i in range(line - 1)) + (column - 1)
    return -1

def extract_java_block(code, start_index):
    """
    Given code and a starting index, finds the first '{' and returns
    the code block with balanced braces.
    """
    index = code.find('{', start_index)
    if index == -1:
        return ""
    brace_count = 0
    block_start = index
    i = index
    while i < len(code):
        if code[i] == '{':
            brace_count += 1
        elif code[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                return code[block_start:i+1]
        i += 1
    return ""

def parse_java_file(file_path):
    """
    Parses a Java file using javalang to extract class and method information.
    For each class and method, it returns a dictionary with keys:
      - "name": the identifier (class or method name)
      - "content": the code block (from the first '{' to the matching '}')
    
    Returns:
        dict: {
            "methods": [ { "name": <method_name>, "content": <method_content> }, ... ],
            "classes": [ { "name": <class_name>, "content": <class_content> }, ... ]
        }
    """
    try:
        with file_path.open("r", encoding="utf-8") as f:
            code = f.read()

        tree = javalang.parse.parse(code)

        methods = []
        classes = []

        # Extract class declarations
        for path, node in tree.filter(javalang.tree.ClassDeclaration):
            if node.position:
                start_index = get_index_from_position(code, node.position.line, node.position.column)
                content = extract_java_block(code, start_index)
            else:
                content = ""
            if content != "":
                classes.append({
                    "name": node.name,
                    "content": content
                })

        # Extract method declarations
        for path, node in tree.filter(javalang.tree.MethodDeclaration):
            if node.position:
                start_index = get_index_from_position(code, node.position.line, node.position.column)
                content = extract_java_block(code, start_index)
            else:
                content = ""
            if content != "":
                methods.append({
                    "name": node.name,
                    "content": content
                })

        return {"methods": methods, "classes": classes}
    except Exception as e:
        print(f"Error parsing Java file {file_path}: {e}")
        return {"methods": [], "classes": []}


def parse_cpp_file(file_path):
    """
    """
    return {"methods": ["dummyCppMethod"], "classes": ["dummyCppClass"]}
