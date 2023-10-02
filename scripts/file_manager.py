
import os
import json
import pandas as pd
from datetime import datetime


def validate_excel_file_path(file_path):
    """Validates the path of the provided Excel file.
    If the file exists and is valid, it returns the content as a pandas DataFrame.
    Otherwise, it raises an appropriate exception.
    """
    if not os.path.exists(file_path) or not file_path.endswith('.xlsx'):
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{file_path}'")

    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        raise e

def validate_mapping_file(file_path):
    """Validates the path of the provided mapping file.
    If the file exists, has a `.json` extension, and contains valid JSON, it returns the parsed JSON data.
    Otherwise, it raises an appropriate exception.
    """
    if not os.path.exists(file_path) or not file_path.endswith('.json'):
        raise FileNotFoundError(f"[Errno 2] No such file or directory or invalid extension: '{file_path}'")

    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data
    except json.JSONDecodeError:
        raise ValueError(f"The file '{file_path}' does not contain valid JSON.")

def validate_schema_file(file_path):
    """
    Validates the provided GraphQL schema file based on basic heuristics.

    Note:
    This function provides a basic level of validation by checking the file's presence,
    its extension, and the existence of some common GraphQL keywords. It does not
    ensure that the file contains a fully valid GraphQL schema. For complete validation,
    a dedicated GraphQL library or tool would be necessary.

    :param file_path: Path to the GraphQL schema file.
    :return: True if basic checks pass, raises an exception otherwise.
    """

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{file_path}'")

    # Check the file extension
    if not file_path.endswith('.ql'):
        raise ValueError(f"Invalid file extension for GraphQL schema: '{file_path}'")

     # Try reading the file as a text file (Replace w/graphene)
    try:
        with open(file_path, 'r') as f:
            _ = f.read()
        return True
    except Exception as e:
        raise ValueError(f"File '{file_path}' could not be read as a text file. Error: {str(e)}")










def find_file(filename_pattern):
    # This function searches the /mnt/data/ directory for a file matching the provided pattern.
    for file in os.listdir("/mnt/data/"):
        if filename_pattern in file:
            return f"/mnt/data/{file}"
    raise FileNotFoundError(f"No file matching the pattern '{filename_pattern}' found.")

def get_latest_file(file_prefix):
    """Given a file prefix, this function looks for the latest file in the /mnt/data/ directory
    that starts with that prefix. It assumes that the files are named in a manner where
    lexicographic sorting aligns with chronological ordering."""
    all_files = os.listdir("/mnt/data/")
    relevant_files = [f for f in all_files if f.startswith(file_prefix)]
    return max(relevant_files) if relevant_files else None

def load_mapping_file(file_path):
    """Loads a mapping file (in JSON format) and returns the data."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def load_excel_data(file_path):
    """Loads an Excel file and returns a DataFrame."""
    return pd.read_excel(file_path)

def load_template_file(file_path):
    """
    Load the contents of a template file.

    Parameters:
    - file_path (str): The path to the template file.

    Returns:
    - str: The contents of the template file.
    """
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def check_script_dependencies(script_names):
    for script in script_names:
        if not os.path.exists(script):
            return False
    return True

# Load the Excel file to inspect its columns
def get_excel_columns(excel_path):
    df = pd.read_excel(excel_path)
    return df.columns.tolist()

# Function to extract source column names from the mapping file
def extract_source_columns_from_mapping(mapping_file_path):
    with open(mapping_file_path, 'r') as f:
        mapping_content = f.read()

    # Parse the JSON content to extract source columns
    mapping_json = json.loads(mapping_content)
    return [field_info["column"] for field_info in mapping_json.values()]

# Validate the Excel columns against the mapping
def validate_columns(excel_path, mapping_path):
    excel_columns = get_excel_columns(excel_path)
    mapping_columns = extract_source_columns_from_mapping(mapping_path)

    # Check if all Excel columns are present in the mapping
    missing_columns = [col for col in excel_columns if col not in mapping_columns]
    return missing_columns

def get_expected_files(hint_file_path):
    """
    Reads from the workflow hint file to determine which files are required and optional.

    Parameters:
        - hint_file_path (str): Path to the workflow hint file.

    Returns:
        - dict: Dictionary containing lists of required and optional files.
    """
    with open(hint_file_path, 'r') as f:
        content = f.read().splitlines()

    required_files = [line.split('=')[1].strip() for line in content if "REQUIRED_FILE" in line]
    optional_files = [line.split('=')[1].strip() for line in content if "OPTIONAL_FILE" in line]

    return {
        'required': required_files,
        'optional': optional_files
    }
    excel_columns = get_excel_columns(excel_path)
    mapping_columns = extract_source_columns_from_mapping(mapping_path)

    # Check if all Excel columns are present in the mapping
    missing_columns = [col for col in excel_columns if col not in mapping_columns]
    return missing_columns

def generate_output_array(data, template_path):
    """Generates the output array for frontend display using a given template."""
    with open(template_path, 'r') as file:
        template = file.read()
    return [template.format(**item) for item in data]

def save_processed_data_to_template(data, template_content, output_file_path):
    """
    Save the processed data using the provided template.

    Parameters:
    - data (list): The processed data to be saved.
    - template_content (str): The content of the template.
    - output_file_path (str): The path where the output file should be saved.

    Returns:
    - None
    """
    # Parsing the template content
    template_json = json.loads(template_content)

    # Getting the actual template string using the "template" key
    template_string = template_json["template"]

    # Formatting the template string with the processed data
    output = template_string.replace('{{data}}', ',\n'.join(json.dumps(item) for item in data))

    # Saving the formatted output to the specified file path
    with open(output_file_path, 'w') as output_file:
        output_file.write(output)

def save_output_array_to_js_file(output_array, output_file_path):
    """Saves the generated output array to a .js file."""
    with open(output_file_path, 'w') as file:
        file.write("data = [\n")
        for item in output_array:
            file.write(json.dumps(item, indent=4))
            file.write(",\n")
        file.write("];")

def extract_expected_data_types_from_mapping(mapping_file_path):
    with open(mapping_file_path, 'r') as file:
        mapping = json.load(file)
    expected_data_types = {}
    for field, config in mapping.items():
        column_name = config["column"]
        expected_data_type = config.get("type", None)
        if expected_data_type:
            expected_data_types[column_name] = expected_data_type
    return expected_data_types




