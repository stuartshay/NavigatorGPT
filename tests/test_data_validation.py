import unittest
import pandas as pd
import json
import sys
import logging
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, '..', 'scripts'))

from file_manager import load_excel_data
from data_validation import (
    validate_excel_data_types_with_df,
    validate_excel_data_values_with_df,
    extract_expected_data_types_from_mapping,
    validate_excel_data_values_with_df,
    cast_dataframe_to_expected_types
)

# Set up the logger
logging.basicConfig(filename='logs/test_log.log', level=logging.INFO)
logger = logging.getLogger()


# Load test configuration
with open("test_config.json", "r") as config_file:
    test_config_data = json.load(config_file)

class TestDataValidation(unittest.TestCase):

    def setUp(self):

        # Ensure the log file is empty before the test
        if os.path.exists('data_validation_errors.log'):
            os.remove('data_validation_errors.log')

        self.valid_excel_path = test_config_data["paths"]["excel_data"]
        self.invalid_excel_path = test_config_data["paths"]["excel_validation_data"]
        self.mapping_file_path = test_config_data["paths"]["mapping_file"]

        self.df_valid = load_excel_data(self.valid_excel_path)
        with open(self.mapping_file_path, "r") as file:
            self.sample_mapping_data = json.load(file)
        with open("mapping/attration.json", "r") as file:
            self.mapping_data = json.load(file)

        # Create a sample dataframe based on the mapping_data fields
        sample_data = {
            'Site Name': ['Site A', 'Site B'],
            'Address': ['123 Elm St', '456 Oak St'],
            'City': ['Anytown', 'Othertown'],
            'State': ['CA', 'TX'],
            'PostalCode': ['12345', '67890'],
            'Country': ['USA', 'USA'],
            'Latitude': [34.0522, 32.7767],
            'Longitude': [-118.2437, -96.7970],
            'Phone': ['123-456-7890', '098-765-4321'],
            'Type': ['Type1', 'Type2'],
            'Status': ['Active', 'Inactive']
        }
        self.df = pd.DataFrame(sample_data)

    def test_extract_data_types(self):
        expected_data_types = {
            key: value['type']
            for key, value in self.sample_mapping_data.items()
            if 'type' in value
        }

        result = extract_expected_data_types_from_mapping(self.mapping_file_path)

        self.assertEqual(result, expected_data_types, "Data types extracted do not match expected values.")

    def test_cast_dataframe_to_expected_types(self):
        # Cast the DataFrame to the expected types
        df_casted = cast_dataframe_to_expected_types(self.df, self.mapping_file_path)

        # Assert the data types
        for column, attributes in self.mapping_data.items():
            if column in df_casted.columns:
                dtype = attributes['type']
                if dtype == 'string':
                    self.assertTrue(all(df_casted[column].apply(type) == str))
                elif dtype == 'integer':
                    self.assertTrue(all(df_casted[column].apply(type) == int))
                elif dtype == 'float':
                    self.assertTrue(all(df_casted[column].apply(type) == float))
                elif dtype == 'boolean':
                    self.assertTrue(all(df_casted[column].apply(type) == bool))

    def test_validate_data_types_valid(self):
      # Cast the dataframe to the expected data types based on the mapping file
      self.df_valid = cast_dataframe_to_expected_types(self.df_valid, self.mapping_file_path)

      # Validate the data types
      errors = validate_excel_data_types_with_df(self.df_valid, self.mapping_file_path)

      # Assert that no errors are found
      self.assertEqual(len(errors), 0, "Expected no errors for matching data types")
      if len(errors) > 0:
        for error in errors:
            print(error)

    def test_validate_allowed_values(self):
         # Load the Excel data
        df_invalid_values = load_excel_data(self.invalid_excel_path)

        # Validate allowed values
        errors = validate_excel_data_values_with_df(df_invalid_values, self.mapping_file_path)

        for error in errors:
          logger.info(error)

        self.assertEqual(len(errors), 15, "Expected 15 errors for invalid values, but found {}.".format(len(errors)))



        # Load the Excel data
        df_invalid = load_excel_data(self.invalid_excel_path)

        # Cast the dataframe to the expected data types based on the mapping file
        df_invalid = cast_dataframe_to_expected_types(df_invalid, self.mapping_file_path)


        # Validate the data types
        try:
          errors = validate_excel_data_types_with_df(df_invalid, self.mapping_file_path)
          if errors:
            for error in errors:
                logger.info(error)
        except TypeError as e:
           logger.info(f"Error: {e}")


if __name__ == "__main__":
    unittest.main()
