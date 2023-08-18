
import pandas as pd
from file_manager import (
    load_mapping_file,
    load_excel_data,
    save_output_array_to_js_file,
    validate_excel_file_path,
    load_template_file,
    save_processed_data_to_template,
)
from data_validation import (
    validate_excel_data_types_with_df,
    process_excel_data_with_mapping,
)

EXCEL_FILE_PATH = "Location-Import.xlsx"
MAPPING_FILE_PATH = "Attration.map"
TEMPLATE_PATH = "display-array.template"
OUTPUT_JS_PATH = "output_array.js"

def main():
    # 1. Load the Excel data
    df = load_excel_data(EXCEL_FILE_PATH)

    # 2. Validate the Excel file path
    validate_excel_file_path(EXCEL_FILE_PATH)

    # 3. Validate the Excel data types
    data_type_validation_results = validate_excel_data_types_with_df(df, MAPPING_FILE_PATH)

    # 4. Process the Excel data with the mapping
    processed_data = process_excel_data_with_mapping(df, load_mapping_file(MAPPING_FILE_PATH))

    # 5. Save the processed data to the template
    save_processed_data_to_template(processed_data, load_template_file(TEMPLATE_PATH), OUTPUT_JS_PATH)

    # 6. Save the output array to a .js file
    save_output_array_to_js_file(processed_data, OUTPUT_JS_PATH)

if __name__ == "__main__":
    main()




