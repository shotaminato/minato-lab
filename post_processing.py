import os, subprocess
from datetime import datetime

# pages directory
SRC_DIR = 'pages'
TARGET_DIR = "modules/ROOT/"

def main():
    # Get the list of files in the pages directory recursively
    for root, dirs, files in os.walk(SRC_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Get created and modified date of the file (yyyy-mm-dd hh:mm:ss)
            modified_timestamp = subprocess.check_output(f'git log --format=%ci -- {file_path} | head -n 1', shell=True).decode().strip()
            created_timestamp  = subprocess.check_output(f'git log --format=%ci -- {file_path} | tail -n 1', shell=True).decode().strip()
            print(f'{file:<40} - Modified Date: {modified_timestamp} - Created Date: {created_timestamp}')
            
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

                    if line[0:2] == "= " or line[0:2] == "# ":
                        write_line = "\n" + line + "\n\n[.text-right]\n投稿日：{postdate}　最終更新日：{revdate}\n\n"
                
                    # Append the processed content to the list
                    processed_content.append(write_line)

                # If the created date is not set, add it to the content
                if not is_cdate_set: processed_content.insert(0, f':postdate: {created_timestamp}\n')
                if not is_mdate_set: processed_content.insert(1, f':revdate: {modified_timestamp}\n')

                os.makedirs(TARGET_DIR + root, exist_ok=True)

                processed_content.insert(0, f"include::partial$template.adoc[]\n\n")

                # Open the file in write mode
                with open(f"{TARGET_DIR}/{root}/{file}", 'w') as wf:
                    # Write the processed content back to the file
                    wf.writelines(processed_content)

if __name__ == '__main__':
    main()