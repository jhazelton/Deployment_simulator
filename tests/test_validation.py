from pathlib import Path
from jim_dply3 import validate_incoming_file

#Test 1
result, file_path = validate_incoming_file(Path("customer_api_v1.zip"))
print("ZIP test:", result)

#Test 2
result, file_path = validate_incoming_file(Path("database_script_v3.sql"))
print("SQL test:", result)

#Test 3
result, file_path = validate_incoming_file(Path("data_insert.txt"))
print("TXT test:", result)


