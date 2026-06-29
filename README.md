# Deployment_simulator
Project overview:
Simulates a deployment orchestration workflow.  The design was inspired by deployment orchestration and release management workflows used on HPE NonStop systems.

Features:
- Input manifest processing
- Artifact validation
- Deployment automation
- Version archiving
- Archive retention policy
- Timestamp logging

Directory Structure:
archived - Stored old copies of deployed files.
deployed - deployed files.
incoming - input files to be deployed by simulator.
jim_logs - contains a log file.

Running Locally:
python3 jim_dply3.py

Running with Docker (and using the Dockerfile):
docker run --rm jim-dply-simulator

Example Output:
Copying file -  incoming/customer_api_v1.zip to   ->  deployed/customer_api_v1.zip
Copying file -  incoming/billing_update_v2.zip to   ->  deployed/billing_update_v2.zip
Copying file -  incoming/frontend_patch.zip to   ->  deployed/frontend_patch.zip
Copying file -  incoming/database_script_v3.sql to   ->  deployed/database_script_v3.sql
Error: Invalid file extension '.txt' on' incoming/data_insert.txt'

Deployment Summary
------------------
Processed: 5
Archived:  0
Failed:    1
Deployed:  4

Expected behavior:
The first run of the deployment simulator will result in no files being copied to Archived folder.
