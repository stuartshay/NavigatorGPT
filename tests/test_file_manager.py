
import unittest
import pandas as pd

# Incorporate the functions from the file_manager.py file for testing

import os
import json
import pandas as pd
from datetime import datetime


def validate_excel_file_path(excel_path):
    """
    Validates if the provided Excel file path exists and is accessible.
    """
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
        return df
    except Exception as e:
        return str(e)

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

def load_excel_file(file_path):
    """Loads an Excel file and returns a DataFrame."""
    return pd.read_excel(file_path)

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







class TestFileManagerComplete(unittest.TestCase):

    def setUp(self):
        # Sample paths for testing
        self.valid_excel_path = "/mnt/data/Location-Import.xlsx"
        self.invalid_excel_path = "/mnt/data/NonExistentFile.xlsx"
        self.mapping_file_path = "/mnt/data/Attration.map"
        self.hint_file_path = "/mnt/data/workflow_hint_1.1.txt"

    # Tests for validate_excel_file_path
    def test_validate_excel_file_path_valid(self):
        result = validate_excel_file_path(self.valid_excel_path)
        self.assertIsInstance(result, pd.DataFrame)

    def test_validate_excel_file_path_invalid(self):
        result = validate_excel_file_path(self.invalid_excel_path)
        self.assertIsInstance(result, str)

    # Tests for find_file
    def test_find_file_valid(self):
        result = find_file("Location-Import.*")
        self.assertEqual(result, self.valid_excel_path)

    def test_find_file_invalid(self):
        with self.assertRaises(FileNotFoundError):
            find_file("NonExistentFile.*")

    # Test for load_mapping_file
    def test_load_mapping_file(self):
        mapping_data = load_mapping_file(self.mapping_file_path)
        self.assertIsInstance(mapping_data, dict)

    # Test for load_excel_file
    def test_load_excel_file(self):
        df = load_excel_file(self.valid_excel_path)
        self.assertIsInstance(df, pd.DataFrame)

    # Test for get_excel_columns
    def test_get_excel_columns(self):
        columns = get_excel_columns(self.valid_excel_path)
        self.assertIsInstance(columns, list)

    # Test for extract_source_columns_from_mapping
    def test_extract_source_columns_from_mapping(self):
        columns = extract_source_columns_from_mapping(self.mapping_file_path)
        self.assertIsInstance(columns, list)

    # Test for validate_columns
    def test_validate_columns(self):
        missing_columns = validate_columns(self.valid_excel_path, self.mapping_file_path)
        self.assertIsInstance(missing_columns, list)

    # Test for get_expected_files
    def test_get_expected_files(self):
        expected_files = get_expected_files(self.hint_file_path)
        self.assertIsInstance(expected_files, dict)
        self.assertIn("required", expected_files)
        self.assertIn("optional", expected_files)

# This is how you'd typically run the tests:
# if __name__ == '__main__':
#     unittest.main()
