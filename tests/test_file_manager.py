
import unittest
import pandas as pd
import json
import sys
import logging
sys.path.append('/home/vagrant/git/NavigatorGPT/scripts/')

from file_manager import validate_excel_file_path
from file_manager import validate_mapping_file
from file_manager import validate_schema_file
from file_manager import load_excel_data

# Set up the logger
logging.basicConfig(filename='logs/test_log.log', level=logging.INFO)
logger = logging.getLogger()

# Loading the test configuration
with open("test_config.json", "r") as config_file:
    test_config_data = json.load(config_file)

class TestFileManager(unittest.TestCase):

    def setUp(self):
        self.valid_excel_path = test_config_data["paths"]["excel_data"]
        self.invalid_excel_path = "data/test/NonExistentFile.xlsx"
        self.valid_mapping_path = test_config_data["paths"]["mapping_file"]
        self.invalid_mapping_path = "mapping/NonExistentMapping.json"
        self.valid_schema_path = test_config_data["paths"]["schema_file"]


    def test_validate_excel_file_path_valid(self):
        result = validate_excel_file_path(self.valid_excel_path)
        self.assertIsInstance(result, pd.DataFrame, "Expected a DataFrame for valid Excel path")

    def test_validate_excel_file_path_invalid(self):
        with self.assertRaises(FileNotFoundError, msg="Expected a FileNotFoundError for invalid Excel path"):
            validate_excel_file_path(self.invalid_excel_path)

    def test_validate_mapping_file_valid(self):
        # Log the directory of the mapping file
        logger.info(f"Validating mapping file at: {self.valid_mapping_path}")

        result = validate_mapping_file(self.valid_mapping_path)
        self.assertIsInstance(result, dict, "Expected a dictionary for valid mapping file")

    def test_validate_schema_file_valid(self):
        """Test if a valid GraphQL schema file is recognized as such."""
        result = validate_schema_file(self.valid_schema_path)
        self.assertTrue(result, "Expected True for valid GraphQL schema file")

    def test_load_excel_data_valid(self):
        df = load_excel_data(self.valid_excel_path)
        self.assertIsInstance(df, pd.DataFrame, "Expected pandas DataFrame for valid Excel file")






if __name__ == '__main__':
    unittest.main()