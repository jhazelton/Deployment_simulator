from datetime import datetime
from pathlib import Path
import shutil

DEPLOYMENT_SOURCE_FILE = Path("deployment_files.txt")
LOG_DIRECTORY = Path("jim_logs")          #contains logs for deployment activities
INCOMING_DIRECTORY = Path("incoming")     #directory containing artifacts to deploy
DESTINATION_DIRECTORY = Path("deployed")  #directory where artifacts are deployed to
ARCHIVED_DIRECTORY = Path("archived")     #contains previous version of deployed artifacts
LOG_OUTPUT_FILE = LOG_DIRECTORY / "dplylogs"
VALID_EXTENSIONS = [".sql", ".zip"]
MAX_HISTORY = 3

def create_directories():
    """Ensure all required directories exist before processing."""
    
    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)
    INCOMING_DIRECTORY.mkdir(parents=True, exist_ok=True)
    DESTINATION_DIRECTORY.mkdir(parents=True, exist_ok=True)
    ARCHIVED_DIRECTORY.mkdir(parents=True, exist_ok=True)

def write_log(log_entry_text):
    """Write timestamped record to the deployment log file."""
    #print("at start of write-log routine") #this statement is only for debugging.

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(LOG_OUTPUT_FILE, "a") as log_stream:
        log_stream.write(f"[{current_time}]   {log_entry_text}\n")
    

def validate_incoming_file(target_filename):

    staging_file = INCOMING_DIRECTORY / target_filename
    
    # printing the value of the staging_file variable.  only for debugging.
    #print(staging_file)

    #check if the file exists
    if not staging_file.exists(): 
        print(f"Error: Target file '{staging_file}' was not found.")
        return False, None

    #check the file extensions
    if staging_file.suffix not in VALID_EXTENSIONS:
        print(f"Error: Invalid file extension '{staging_file.suffix}' on' {staging_file}'")
        return False, None
            
    return True, staging_file

def cleanup_archives(target_filename):

    base_name = Path(target_filename).stem

    archive_files = list(
        ARCHIVED_DIRECTORY.glob(f"{base_name}_*{Path(target_filename).suffix}")
    )

    archive_files.sort(key=lambda f: f.stat().st_mtime)
    if len(archive_files) > MAX_HISTORY:
        files_to_delete = archive_files[:-MAX_HISTORY]
        for old_file in files_to_delete:
            write_log(f"Removing archived file: {old_file.name}")
            old_file.unlink()


def main():
    ARCHIVE_COUNTER = 0
    FAILED_COUNTER = 0
    PROCESSED_COUNTER = 0
    SUCCESSFUL_DEPLOYMENT_COUNTER = 0

    create_directories()

    # verify that input file exists and is NOT empty before opening
    #  the file for read.
    if not DEPLOYMENT_SOURCE_FILE.exists():       
        print(f"Error: Target file '{DEPLOYMENT_SOURCE_FILE}' was not found.")
        return

    if DEPLOYMENT_SOURCE_FILE.stat().st_size == 0:
        print(f"Error: Input file '{DEPLOYMENT_SOURCE_FILE}' is completely empty (0 bytes).")
        return

    with open(DEPLOYMENT_SOURCE_FILE, "r") as deployment_stream:
        
        for raw_line in deployment_stream:
            target_filename = raw_line.strip()

            write_log(f"Starting Deployment:    {target_filename}")

            if target_filename:
                is_valid, staging_path = validate_incoming_file(target_filename)

                PROCESSED_COUNTER += 1   # Increments count by 1

                if is_valid:
                    destination_file = DESTINATION_DIRECTORY / target_filename
                    
                    write_log(f"Validation Successful:  {target_filename}")
                    
                    # Check if a file already exists in the deployed folder
                    if destination_file.exists():
                        print(f"Archiving existing version of: {target_filename}")
                        timestamp = datetime.now().strftime("_%Y%m%d_%H%M%S")

                        archived_filename = (
                            f"{destination_file.stem}"
                            f"{timestamp}"
                            f"{destination_file.suffix}"
                        )

                        archive_file = ARCHIVED_DIRECTORY / archived_filename

                        # Move the existing version in deployed folder to the archive folder
                        shutil.move(destination_file, archive_file)

                        ARCHIVE_COUNTER += 1  # Increments count by 1

                        cleanup_archives(target_filename)

                        write_log(f"Archived existing file: {target_filename}")

                    print(f"Copying file -  {staging_path} to   ->  {destination_file}")
                    shutil.copy(staging_path, destination_file)

                    SUCCESSFUL_DEPLOYMENT_COUNTER += 1   # Increments count by 1

                    write_log(f"Success. All actions completed for: {target_filename}")

                else:
                    FAILED_COUNTER += 1  # Increments count by 1

    print()
    print("Deployment Summary")
    print("------------------")
    print(f"Processed: {PROCESSED_COUNTER}")
    print(f"Archived:  {ARCHIVE_COUNTER}")
    print(f"Failed:    {FAILED_COUNTER}")
    print(f"Deployed:  {SUCCESSFUL_DEPLOYMENT_COUNTER}")

    write_log("Deployment Summary")
    write_log(f"Processed: {PROCESSED_COUNTER}")
    write_log(f"Archived:  {ARCHIVE_COUNTER}")
    write_log(f"Failed:    {FAILED_COUNTER}")
    write_log(f"Deployed:  {SUCCESSFUL_DEPLOYMENT_COUNTER}")

if __name__ == "__main__":
    main()