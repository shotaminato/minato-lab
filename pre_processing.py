import os, subprocess, shutil
from datetime import datetime

# pages directory
SRC_DIR = 'ROOT'
TARGET_DIR = "modules"

def main():
    # Copy dir to the target dir
    os.makedirs(f'{TARGET_DIR}/{SRC_DIR}', exist_ok=True)
    
    shutil.copy2   (f"{SRC_DIR}/nav.adoc", f"{TARGET_DIR}/{SRC_DIR}/nav.adoc")
    shutil.copytree(f"{SRC_DIR}/images"  , f"{TARGET_DIR}/{SRC_DIR}/images"  , dirs_exist_ok=True)
    shutil.copytree(f"{SRC_DIR}/partials", f"{TARGET_DIR}/{SRC_DIR}/partials", dirs_exist_ok=True)

    # Walk through the pages directory
    for cur_dir, dirs, files in os.walk(f"{SRC_DIR}/pages"):
        for file in files:
            file_path = os.path.join(cur_dir, file)
            
            # Get created and modified date of the file (yyyy-mm-dd hh:mm:ss)
            modified_timestamp = subprocess.check_output(f'git log --format=%ci -- {file_path} | head -n 1', shell=True).decode().strip()
            created_timestamp  = subprocess.check_output(f'git log --format=%ci -- {file_path} | tail -n 1', shell=True).decode().strip()
            print(f'{file:<40} - Modified Date: {modified_timestamp} - Created Date: {created_timestamp}')
            
            modified_timestamp = f"{modified_timestamp[0:4]}年{modified_timestamp[5:7]}月{modified_timestamp[8:10]}日"
            created_timestamp  = f"{created_timestamp [0:4]}年{created_timestamp [5:7]}月{created_timestamp [8:10]}日"

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
                        write_line = "\n" + line + "\n\n[.text-right]\n投稿日：{postdate} &#160;&#160;&#160;&#160; 最終更新日：{revdate}\n\n"
                
                    # Append the processed content to the list
                    processed_content.append(write_line)

                # If the created date is not set, add it to the content
                if not is_cdate_set: processed_content.insert(0, f':postdate: {created_timestamp}\n')
                if not is_mdate_set: processed_content.insert(1, f':revdate: {modified_timestamp}\n')

                os.makedirs(f'{TARGET_DIR}/{cur_dir}', exist_ok=True)

                processed_content.insert(0, f"include::partial$template.adoc[]\n\n")

                # Open the file in write mode
                with open(f"{TARGET_DIR}/{cur_dir}/{file}", 'w') as wf:
                    # Write the processed content back to the file
                    wf.writelines(processed_content)

if __name__ == '__main__':
    main()