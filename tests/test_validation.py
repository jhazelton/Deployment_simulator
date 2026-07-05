from pathlib import Path
from jim_dply3 import validate_incoming_file

#Test 1
def test_zip_file_validation():
    # Arrange
    result, file_path = validate_incoming_file(Path("customer_api_v1.zip"))

    # Assert 
    assert result is True

#Test 2
def test_sql_file_validation():
    # Arrange
    result, file_path = validate_incoming_file(Path("database_script_v3.sql"))

    # Assert
    assert result is True

#Test 3
def test_txt_file_validation():
    # Arrange
    result, file_path = validate_incoming_file(Path("data_insert.txt"))

    # Assert
    assert result is True
