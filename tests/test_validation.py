import sys
sys.path.append('./scripts')  # Add the path to your script folder
from data_validation import check_file_presence


sys.path.append('path_to_your_script_folder')  # Add the path to your script folder if it's not already in sys.path

from data_validation import check_file_presence  # Adjust the import based on your script's structure

def test_check_file_presence():
    required_files = ['file_that_exists.xlsx']
    optional_files = ['file_that_doesnt_exist.map']
    missing_required, missing_optional = check_file_presence(required_files, optional_files)

    assert not missing_required, "Required files are missing!"
    assert 'file_that_doesnt_exist.map' in missing_optional, "Optional file check failed!"
