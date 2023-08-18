import json
import pandas as pd

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

def validate_excel_data_types_with_df(df, mapping_file_path):
    expected_data_types = extract_expected_data_types_from_mapping(mapping_file_path)
    for column, expected_dtype in expected_data_types.items():
        if column in df.columns:
            actual_dtype = df[column].dtype.name
            if actual_dtype == "object":
                actual_dtype = "string"
            if actual_dtype != expected_dtype:
                raise TypeError(f"Expected {column} to have dtype {expected_dtype}, but found {actual_dtype}.")
    return True

def convert_data_types_according_to_updated_mapping(df, mapping_data):
    for field, config in mapping_data.items():
        expected_data_type = config.get("type")
        if expected_data_type and config["column"] in df.columns:
            if expected_data_type == "string":
                df[config["column"]] = df[config["column"]].astype(str)
    return df

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

def validate_excel_data_with_mapping(excel_data, mapping):
    """
    Validates the columns and data in an Excel file against a provided mapping.

    Parameters:
    - excel_data (pd.DataFrame): Data from the Excel file.
    - mapping (dict): The mapping defining columns and their expected data types.

    Returns:
    - tuple: A tuple containing a boolean indicating validity and an error message (if any).
    """
    # Check if all required columns from the mapping are present in the Excel data
    missing_columns = [col for col in mapping if col not in excel_data.columns and mapping[col]['isRequired']]
    if missing_columns:
        return False, f"Missing columns: {', '.join(missing_columns)}"

    # Check data types (this is a basic check and can be expanded based on the structure of your mapping)
    for col, col_info in mapping.items():
        if col in excel_data.columns and col_info['type'] != str(excel_data[col].dtype):
            return False, f"Data type mismatch for column {col}. Expected {col_info['type']} but found {excel_data[col].dtype}"

    return True, None

def enforce_data_types_based_on_graphql(df, graphql_schema):
    """
    Enforces data types based on the GraphQL schema.

    Parameters:
        - df (pd.DataFrame): DataFrame containing the data from the Excel file.
        - graphql_schema (str): String content of the GraphQL schema.

    Returns:
        - pd.DataFrame: DataFrame with enforced data types.
    """
    return df

def validate_excel_file_columns(excel_columns, mapping_data, graphql_schema):
    """
    Validate Excel columns against the mapping file and GraphQL schema.

    Parameters:
    - excel_columns: List of columns present in the Excel file.
    - mapping_data: Dictionary containing the mapping data.
    - graphql_schema: String containing the GraphQL schema.

    Returns:
    - A success message if the columns match.
    - An error message highlighting discrepancies if they don't match.
    """
    # Extracting columns from the mapping data and GraphQL schema
    mapping_columns = list(mapping_data.keys())
    graphql_columns = [line.split(":")[0].strip() for line in graphql_schema.split("\n") if ":" in line]

    # Checking if any Excel column is missing in the mapping file or GraphQL schema
    missing_in_mapping = [col for col in excel_columns if col not in mapping_columns]
    missing_in_graphql = [col for col in excel_columns if col not in graphql_columns]

    if missing_in_mapping:
        return f"Error: The following columns from Excel are missing in the mapping file: {', '.join(missing_in_mapping)}"

    if missing_in_graphql:
        return f"Error: The following columns from Excel are missing in the GraphQL schema: {', '.join(missing_in_graphql)}"

    return "Excel columns successfully validated against mapping file and GraphQL schema."

def extract_expected_data_types_from_mapping(mapping_file_path):
    """Extracts the expected data types of columns from the mapping file."""
    with open(mapping_file_path, 'r') as f:
        mapping_data = json.load(f)
    expected_data_types = {key: value['validation']['type'] for key, value in mapping_data.items() if 'validation' in value}
    return expected_data_types

def process_excel_data_with_mapping(df, mapping_data):
    """
    Processes the excel data according to the provided mapping.

    Parameters:
        - df (pd.DataFrame): The excel data in dataframe format.
        - mapping_data (dict): The mapping data.

    Returns:
        - list: A list of dictionaries containing the processed data.
    """
    output_array = []
    for index, row in df.iterrows():
        document = {}
        for field, config in mapping_data.items():
            if config["column"] not in df.columns and not config["isRequired"]:
                continue  # Skip the column if it's not required and missing in the Excel data
            if "dependency" in config:
                # If there's a dependency defined, use the mapping
                dependency_field = config["dependency"]["fieldName"]
                dependency_mapping = config["dependency"]["mapping"]
                if row[dependency_field] in dependency_mapping:
                    document[config["documentField"]] = dependency_mapping[row[dependency_field]]
                else:
                    document[config["documentField"]] = None
            else:
                # Otherwise, use the direct mapping
                document[config["documentField"]] = row[config["column"]]
        output_array.append(document)
    return output_array