import pandas as pd
import json
import os
import re

def get_mapping_data(mapping_file_path):
    """Reads the mapping file and returns its content as a dictionary.
    If an error occurs, it returns a string with the error description."""
    try:
        with open(mapping_file_path, 'r') as file:
            mapping_data = json.load(file)
        return mapping_data
    except Exception as e:
        return str(e)




def check_file_presence(required_files, optional_files=[]):
    """
    Checks the presence of required and optional files.

    Parameters:
        - required_files (list): List of paths to required files.
        - optional_files (list): List of paths to optional files.

    Returns:
        - tuple: (list of missing required files, list of missing optional files)
    """
    missing_required = [file for file in required_files if not os.path.exists(file)]
    missing_optional = [file for file in optional_files if not os.path.exists(file)]

    return missing_required, missing_optional

def extract_expected_data_types_from_mapping(mapping_file_path):
    """
    Extracts source column names and their expected data types from the mapping file.

    Parameters:
        - mapping_file_path (str): Path to the mapping file.

    Returns:
        - dict: Dictionary with column names as keys and expected data types as values.
    """
    with open(mapping_file_path, 'r') as f:
        mapping_content = f.read()

    # Parse the JSON content to extract source columns and their expected types
    mapping_json = json.loads(mapping_content)
    # Ensure 'validation' key exists and then extract the 'type'
    return {field_info["column"]: field_info["validation"]["type"] for field_info in mapping_json.values() if "validation" in field_info}

def validate_excel_data_types_with_df(df, mapping_path):
    """
    Validates data types of all columns in the provided DataFrame using the mapping.

    Parameters:
        - df (pd.DataFrame): DataFrame containing the Excel data.
        - mapping_path (str): Path to the mapping file.

    Returns:
        - dict: Dictionary with column names as keys and 'Valid' or 'Invalid' as values.
    """
    # Extract the expected data types from the mapping file using the final version of the helper function
    expected_data_types = extract_expected_data_types_from_mapping(mapping_path)

    # Convert any "string" values to "object" to match pandas DataFrame dtypes
    for key, value in expected_data_types.items():
        if value == "string":
            expected_data_types[key] = "object"

    validation_results = {}

    # Iterate over the columns in the DataFrame and check data types
    for column in df.columns:
        actual_dtype = str(df[column].dtype)
        if column in expected_data_types and actual_dtype == expected_data_types[column]:
            validation_results[column] = "Valid"
        elif column not in expected_data_types:
            validation_results[column] = f"Column not in expected list. Actual dtype: {actual_dtype}"
        else:
            validation_results[column] = f"Invalid (Expected: {expected_data_types[column]}, Actual: {actual_dtype})"

    return validation_results

def adjusted_validate_excel_data_types_with_df_v2(df, mapping_file_path):
    """
    Further adjusted function to handle specific issues raised and ensure the 'validation' key exists:
    1. Accept any column present in the Excel file, even if not initially in our expected list.
    2. Convert integers to strings during validation if the expected data type is a string.
    """
    # Load the mapping file
    with open(mapping_file_path, 'r') as f:
        mapping_data = json.load(f)

    expected_data_types = {}
    for key, value in mapping_data.items():
        if 'validation' in value and 'type' in value['validation']:
            expected_type = value['validation']['type']
            if expected_type == "number":
                expected_type = "float64"  # Since Excel might interpret numbers as floats
            elif expected_type == "string":
                expected_type = "object"
            expected_data_types[key] = expected_type

    issues = {}

    for column in df.columns:
        actual_dtype = df[column].dtype.name
        expected_dtype = expected_data_types.get(column)

        # Adjusting for the PostalCode scenario and similar cases
        if column == "PostalCode" and actual_dtype == "int64" and expected_dtype == "object":
            df[column] = df[column].astype(str)
            actual_dtype = "object"

        if expected_dtype:
            if actual_dtype != expected_dtype:
                issues[column] = f"Expected {expected_dtype}, but found {actual_dtype}."

        # If the column was not in the expected list but is present in the mapping, it's acceptable
        elif column in mapping_data:
            continue
        else:
            issues[column] = f"Not in the expected list. Found data type: {actual_dtype}."

    return issues

def adjusted_validate_excel_data_types_with_df_v3(df, mapping_file):
    """Adjusted function to validate the Excel data types against the mapping file.
    This function assumes all Excel values are strings and validates accordingly.
    It reads the data type expectations from the mapping file and checks if the Excel data
    matches those expectations.
    Returns a dictionary with column names as keys and encountered data types as values
    for columns that did not match the expected data types."""
    # Get the mapping data from the provided mapping file
    mapping_data = get_mapping_data(mapping_file)

    if isinstance(mapping_data, str):
        return f"Error reading mapping file: {mapping_data}"

    # Extract the expected data types from the mapping data
    expected_data_types = {item['column']: item['validation']['type'] for item in mapping_data.values() if 'validation' in item}

    # Convert all int64 data types in the DataFrame to string, to handle cases where numbers are used as strings
    for column in df.columns:
        if df[column].dtype == 'int64':
            df[column] = df[column].astype(str)

    # Check the data types of each column in the DataFrame
    encountered_data_types = {column: df[column].dtype for column in df.columns if column in expected_data_types}

    # Identify columns that do not have the expected data type
    mismatched_columns = {column: dtype for column, dtype in encountered_data_types.items() if dtype != 'object'}

    return mismatched_columns

def validate_excel_data_types(excel_path, mapping_path):
    """
    Validates data types of all columns in the Excel file using the mapping.

    Parameters:
        - excel_path (str): Path to the Excel file.
        - mapping_path (str): Path to the mapping file.

    Returns:
        - dict: Dictionary with column names as keys and 'Valid' or 'Invalid' as values.
    """
    # Extract the expected data types from the mapping file
    expected_data_types = extract_expected_data_types_from_mapping(mapping_path)

    # Load the Excel file with specific dtype for columns defined as strings in the mapping
    string_columns = [col for col, dtype in expected_data_types.items() if dtype == "object"]
    df = pd.read_excel(excel_path, dtype={col: str for col in string_columns})

    validation_results = {}

    # Iterate over the columns in the Excel file and check data types
    for column in df.columns:
        actual_dtype = str(df[column].dtype)
        if column in expected_data_types and actual_dtype == expected_data_types[column]:
            validation_results[column] = "Valid"
        elif column not in expected_data_types:
            validation_results[column] = f"Column not in expected list. Actual dtype: {actual_dtype}"
        else:
            validation_results[column] = f"Invalid (Expected: {expected_data_types[column]}, Actual: {actual_dtype})"

    return validation_results

def broad_validate_against_graphql_schema(df_columns, graphql_schema_contents):
    """
    Validates the columns of the DataFrame against the fields in the entire GraphQL schema,
    without considering specific nested structures.

    Parameters:
        - df_columns (list): List of columns in the DataFrame.
        - graphql_schema_contents (str): Content of the GraphQL schema.

    Returns:
        - dict: Dictionary with column names as keys and 'Valid' or 'Invalid' as values.
    """
    validation_results = {}

    for column in df_columns:
        if column in graphql_schema_contents:
            validation_results[column] = "Valid"
        else:
            validation_results[column] = "Invalid: Column not found anywhere in GraphQL schema"

    return validation_results

def check_extra_columns(df_columns, mapping_path):
    """
    Checks for any extra columns in the Excel file that are not defined in the mapping file.

    Parameters:
        - df_columns (list): List of columns in the DataFrame (Excel file).
        - mapping_path (str): Path to the mapping file.

    Returns:
        - list: List of extra columns present in the Excel file but not in the mapping.
    """
    # Extract expected columns from the mapping file
    with open(mapping_path, 'r') as f:
        mapping = json.load(f)
    expected_columns = list(mapping.keys())

    # Identify extra columns in the Excel file
    extra_columns = [col for col in df_columns if col not in expected_columns]

    return extra_columns

def enforce_data_types_based_on_graphql(df, graphql_schema):
    """
    Enforces data types based on the GraphQL schema.

    Parameters:
        - df (pd.DataFrame): DataFrame containing the data from the Excel file.
        - graphql_schema (str): String content of the GraphQL schema.

    Returns:
        - pd.DataFrame: DataFrame with enforced data types.
    """
    # Extract type definitions from the GraphQL schema
    type_defs = re.findall(r"type (\w+) {([\s\S]*?)}", graphql_schema)

    # Build a dictionary of field names and their types
    field_types = {}
    for type_def in type_defs:
        type_name, fields = type_def
        fields = re.findall(r"(\w+): (\w+)", fields)
        for field, field_type in fields:
            field_types[field] = field_type

    # Convert DataFrame columns based on GraphQL types
    for col in df.columns:
        if col in field_types:
            graphql_type = field_types[col]
            if graphql_type == "String":
                df[col] = df[col].astype(str)
            elif graphql_type == "Int":
                df[col] = df[col].astype(int)
            elif graphql_type == "Float":
                df[col] = df[col].astype(float)
            # ... add more type conversions as needed
        else:
            print(f"Warning: Column {col} not found in GraphQL schema. No type enforcement applied.")

    return df
