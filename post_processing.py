import os, subprocess
from datetime import datetime

# pages directory
PAGES_DIR = 'modules/ROOT/pages'

def main():
    # Get the list of files in the pages directory recursively
    for root, dirs, files in os.walk(PAGES_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Get modified date of the file (yyyy-mm-dd hh:mm:ss)
            modified_timestamp = subprocess.check_output(f'git log --format=%ci -- {file_path} | head -n 1', shell=True).decode().strip()

            # Get created date of the file using git command
            created_timestamp = subprocess.check_output(f'git log --format=%ci -- {file_path} | tail -n 1', shell=True).decode().strip()

            # Print the modified and created date in the format yyyy-mm-dd hh:mm:ss
            print(f'{file:<40} - Modified Date: {modified_timestamp} - Created Date: {created_timestamp}')
            
            # Get the full path of the file
            file_path = os.path.join(root, file)
            # Open the file in read mode
            with open(file_path, 'r') as f:
                is_cdate_set = False
                is_mdate_set = False

                processed_content = []

                # Process the content
                for line in f:
                    write_line = line
                    # Check if the created date is already set
                    if ':postdate:' in line:
                        is_cdate_set = True
                        write_line = f':postdate: {created_timestamp}\n'
                    if ':revdate:' in line:
                        is_mdate_set = True
                        write_line = f':revdate: {modified_timestamp}\n'
                
                    # Append the processed content to the list
                    processed_content.append(write_line)

                # If the created date is not set, add it to the content
                if not is_cdate_set:
                    processed_content.insert(0, f':postdate: {created_timestamp}\n')
                
                if not is_mdate_set:
                    processed_content.insert(1, f':revdate: {modified_timestamp}\n')

                # Open the file in write mode
                with open(file_path, 'w') as wf:
                    # Write the processed content back to the file
                    wf.writelines(processed_content)

if __name__ == '__main__':
    main()