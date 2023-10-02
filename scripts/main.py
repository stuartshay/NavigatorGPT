
import pandas as pd
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from file_manager import (
    validate_excel_file_path,
    validate_mapping_file,
    validate_schema_file,
    load_mapping_file,
    load_excel_data,
    save_output_array_to_js_file,
    load_template_file,
    save_processed_data_to_template,
)
from data_validation import (
    cast_dataframe_to_expected_types,
    validate_excel_data_types_with_df,
    validate_excel_data_values_with_df,
    handle_validation_errors,
    process_excel_data_with_mapping,
)

EXCEL_FILE_PATH = "Location-Import.xlsx"
MAPPING_FILE_PATH = "attration.json"
TEMPLATE_PATH = "display-array.template"
SCHEMA_FILE_PATH = "Attraction.ql"
OUTPUT_JS_PATH = "output_array.js"

def main():

    # 1. Validate the Necessary file paths
    validate_excel_file_path(EXCEL_FILE_PATH)
    validate_mapping_file(MAPPING_FILE_PATH)
    validate_schema_file(SCHEMA_FILE_PATH)

    # 2. Load the Excel data
    df = load_excel_data(EXCEL_FILE_PATH)

    # 3. Validate data values based on allowed values, patterns etc.
    data_value_validation_results = validate_excel_data_values_with_df(df, MAPPING_FILE_PATH)

    # 4. Handle the validation errors
    df = handle_validation_errors(df, data_value_validation_results)

    # 5. Validate the Excel data types
    data_type_validation_results = validate_excel_data_types_with_df(df, MAPPING_FILE_PATH)

    # 6. Cast to the Correct Data Type
    df = cast_dataframe_to_expected_types(df, MAPPING_FILE_PATH)

    # 7. Process the Excel data with the mapping
    processed_data = process_excel_data_with_mapping(df, load_mapping_file(MAPPING_FILE_PATH))

    # 8. Save the processed data to the template
    save_processed_data_to_template(processed_data, load_template_file(TEMPLATE_PATH), OUTPUT_JS_PATH)

    # 9. Save the output array to a .js file
    save_output_array_to_js_file(processed_data, OUTPUT_JS_PATH)

if __name__ == "__main__":
    main()




