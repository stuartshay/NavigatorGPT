import file_manager
import data_validation

def main():
    # Step 1: Check for necessary files
    file_manager.check_for_necessary_files()

    # Step 2: Load data from Excel
    df = file_manager.load_excel_data()

    # Step 3: Validate data types
    data_validation.validate_data_types(df)

    # Step 4: Validate column names
    data_validation.validate_column_names(df)

    # Step 5: Preview rows
    preview_rows = data_validation.preview_rows(df)

    # Step 6: Validate data values
    data_validation.validate_data_values(df)

    # Step 7: Generate output
    output_data = data_validation.generate_output(df, preview_rows)

    return output_data

if __name__ == "__main__":
    main()


